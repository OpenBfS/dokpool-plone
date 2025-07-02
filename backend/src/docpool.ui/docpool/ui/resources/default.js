import "bootstrap";
import React, {useState, useRef, useEffect} from "react";
import {createRoot} from "react-dom/client";
// TODO Can be removed already compiled with webpack?
import "./docpool.scss";

const Listing = ({items, modified}) => {
  const [data, setData] = useState([]);
  const buttonRefs = useRef({});
  const [hasNewData, setHasNewData] = useState(false);
  const [modified_since, setModifiedSince] = useState(modified);
  const eventHandlers = useRef({});

  const changeItemByUid = (uidToChange) => {
    setData(prevData => {

      // Find element
      const indexToChange = prevData.findIndex(item => item && item.uid === uidToChange);

      // Not found
      if (indexToChange === -1) {
        return prevData;
      }

      const newData = [...prevData];
      const currentItem = newData[indexToChange];

      // Temp DOM-Element
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = currentItem.html;

      // Find status display
      const status_display = tempDiv.querySelector('.card-text.text-uppercase.small');

      if (status_display) {
        status_display.textContent = 'public';

        // Update HTML
        newData[indexToChange] = {
          ...currentItem,
          html: tempDiv.innerHTML
        };
      }

      return newData;

    });
  };

  const setWFStatus = async (itemUrl, uid) => {
    const response = await fetch(itemUrl + "/@workflow/publish", {
      method: "POST",
      headers: {
        "Accept": "application/json",
      },
    });
    changeItemByUid(uid);
  }

  // Init fetch with first items
  useEffect(() => {
    const fetchData = async () => {
      // Parse items inside the effect to avoid re-parsing on every render
      const parsedItems = JSON.parse(items);
      const urls = parsedItems.map((item) => `http://localhost:8080/Plone/listing-item?uid=${item}`);
      // Empty the data array
      setData(new Array(urls.length).fill(null));

      // Process each URL
      urls.forEach(async (url, index) => {
        try {
          const response = await fetch(url);
          const html = await response.text();

          // Update items in the array
          setData(prevData => {
            const newData = [...prevData];
            newData[index] = {html, uid: parsedItems[index]};
            return newData;
          });
        } catch (error) {
          console.error(`Error on URL ${url}`, error);
        }
      });
    };

    fetchData();
  }, [items]);

  // Add event listener to all buttons
  useEffect(() => {
    Object.keys(buttonRefs.current).forEach(key => {
      const button = buttonRefs.current[key];
      if (button) {
        // Create a handler function and store it in the ref
        if (!eventHandlers.current[key]) {
          eventHandlers.current[key] = (e) => {
            e.preventDefault();
            setWFStatus(button.dataset.itemUrl, button.dataset.itemUid);
          };
        }
        button.addEventListener('click', eventHandlers.current[key]);
      }
    });

    // Cleanup
    return () => {
      Object.keys(buttonRefs.current).forEach(key => {
        const button = buttonRefs.current[key];
        if (button && eventHandlers.current[key]) {
          button.removeEventListener('click', eventHandlers.current[key]);
        }
      });
    };
  }, [data]);


  useEffect(() => {

    const checkForNewData = async () => {
      console.log('poll');
      try {
        const response = await fetch('http://localhost:8080/Plone/@new-data-check', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({modified_since: modified_since}),
        });

        const result = await response.json();

        console.log('poll');
        // New data?
        if (result.hasNewData) {
          setHasNewData(true);
        }

      } catch (error) {
        console.error('Fehler beim Prüfen auf neue Daten:', error);
      }
    };

    const pollingInterval = setInterval(checkForNewData, 10000);

    // Cleanup - Needed?
    return () => clearInterval(pollingInterval);
  }, []);

  // Funktion zum Aktualisieren der Daten, wenn neue verfügbar sind
  const refreshData = () => {
    window.location.reload();

    setHasNewData(false);
  };


  return (
    <div>
      {hasNewData && (
        <div className="new-data-notification">
          <div className="alert alert-info" role="alert">
            Neue Daten sind verfügbar!
            <button
              className="btn btn-link"
              onClick={refreshData}
            >
              Jetzt aktualisieren
            </button>
          </div>
        </div>
      )}
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item === null ? (
              <span>Wird geladen...</span>
            ) : (
              <div dangerouslySetInnerHTML={{__html: item.html}}
                   ref={el => {
                     // Search for Button an assign ref
                     if (el) {
                       buttonRefs.current[index] = el.querySelector('a.dropdown-item.publish');
                     }
                   }}
              ></div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

const root = document.getElementById("docpool-listing");
const react_root = createRoot(root);
react_root.render(<Listing items={root.getAttribute("data-listing-items")}
                  modified={root.getAttribute("data-listing-modified")}/>);
