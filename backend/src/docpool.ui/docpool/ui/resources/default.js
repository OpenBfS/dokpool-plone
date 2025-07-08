import "bootstrap";
import React, {useState, useRef, useEffect} from "react";
import {createRoot} from "react-dom/client";
// TODO Can be removed already compiled with webpack?
import "./docpool.scss";

const Listing = ({items, modified}) => {
  const [data, setData] = useState([]);
  const [itemUids, setItemUids] = useState([]);
  const buttonRefs = useRef({});
  const [hasNewData, setHasNewData] = useState(false);
  const [modified_since, setModifiedSince] = useState();
  const eventHandlers = useRef({});

  // Items beim ersten Laden items & modified in den State laden
  useEffect(() => {
    try {
      const parsedItems = JSON.parse(items);
      setItemUids(parsedItems);
    } catch (error) {
      console.error('Fehler beim Parsen der Items:', error);
      setItemUids([]);
    }
    setModifiedSince(modified);
  }, []);

  // Fetch data when itemUids change
  useEffect(() => {
    fetchData();
  }, [itemUids]);

  const fetchData = async () => {
    if (itemUids.length === 0) return;

    const urls = itemUids.map((uid) => `http://localhost:8080/Plone/listing-item?uid=${uid}`);
    // Empty the data array
    setData(new Array(urls.length).fill(null));

    // Process each URL
    urls.forEach(async (url, index) => {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          alert(`Error ${response.statusText}`);
          throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
        }
        const html = await response.text();

        // Update items in the array
        setData(prevData => {
          const newData = [...prevData];
          newData[index] = {html, uid: itemUids[index]};
          return newData;
        });
      } catch (error) {
        console.error(`Error on URL ${url}`, error);
      }
    });
  };

  const setWFStatus = async (itemUrl, uid) => {
    const response = await fetch(itemUrl + "/@workflow/publish", {
      method: "POST",
      headers: {
        "Accept": "application/json",
      },
    });
    if (!response.ok) {
      alert(`Error ${response.statusText}`);
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }
    await fetchData();
  }


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

  const checkForNewData = async () => {
    try {
      const response = await fetch('http://localhost:8080/Plone/@new-data-check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({modified_since: modified_since}),
      });

      if (!response.ok) {
        alert(`Error ${response.statusText}`);
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();

      // New data?
      if (result.modified_last > modified_since) {
        setHasNewData(true);
      }
      return result.modified_last;

    } catch (error) {
      console.error('Fehler beim Prüfen auf neue Daten:', error);
    }
  };

  useEffect(() => {
    const pollingInterval = setInterval(() => {
          console.log('polling');
          checkForNewData();
        },10000);
    // Cleanup - Needed?
    return () => clearInterval(pollingInterval);
  }, [modified_since]);

  // Funktion zum Aktualisieren der Daten, wenn neue verfügbar sind
  const refreshData = async () => {
    // Fetch new items
    fetchData();
    // Fetch new modified and update state
    const new_modified = await checkForNewData()
    setModifiedSince(new_modified)
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
