import "bootstrap";
import React, {useState, useRef, useEffect} from "react";
import {createRoot} from "react-dom/client";
import "./base.scss";

const Listing = ({items}) => {
  const [data, setData] = useState([]);
  const [filter, setFilter] = useState("all");
  const buttonRefs = useRef({});
  const eventHandlers = useRef({});

  useEffect(() => {
    const fetchData = async () => {
      // Parse items inside the effect to avoid re-parsing on every render
      const parsedItems = JSON.parse(items);
      const urls = parsedItems.map((item) => `http://localhost:8080/Plone/listing-item?title=${item}`);
      console.log(urls);

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
            newData[index] = { html, title: parsedItems[index] };
            return newData;
          });
        } catch (error) {
          console.error(`Error on URL ${url}`, error);
        }
      });
    };

    fetchData();
  }, [items]);

  useEffect(() => {
    // Add event listener to all buttons
    Object.keys(buttonRefs.current).forEach(key => {
      const button = buttonRefs.current[key];
      if (button) {
        // Create a handler function and store it in the ref
        if (!eventHandlers.current[key]) {
          eventHandlers.current[key] = (e) => {
            e.preventDefault();
            console.log(`Button ${key} wurde geklickt!`);
          };
        }
        // Add the event listener using the stored handler
        button.addEventListener('click', eventHandlers.current[key]);
      }
    });

    // Cleanup
    return () => {
      Object.keys(buttonRefs.current).forEach(key => {
        const button = buttonRefs.current[key];
        if (button && eventHandlers.current[key]) {
          // Remove the event listener using the same handler reference
          button.removeEventListener('click', eventHandlers.current[key]);
        }
      });
    };
  }, [data]);

  // Filter the data based on the selected filter
  const filteredData = data.map((item, index) => {
    // If filter is "all" or the item's title matches the filter, include it
    if (filter === "all" || (item && item.title === filter)) {
      return { item, index };
    }
    return null;
  }).filter(Boolean);

  return (
    <div>
      <div className="filter-controls mb-3">
        <div className="btn-group" role="group" aria-label="Filter options">
          <button
            type="button"
            className={`btn btn-outline-primary ${filter === "all" ? "active" : ""}`}
            onClick={() => setFilter("all")}
          >
            Alle
          </button>
          <button
            type="button"
            className={`btn btn-outline-primary ${filter === "1" ? "active" : ""}`}
            onClick={() => setFilter("1")}
          >
            1
          </button>
          <button
            type="button"
            className={`btn btn-outline-primary ${filter === "2" ? "active" : ""}`}
            onClick={() => setFilter("2")}
          >
            2
          </button>
          <button
            type="button"
            className={`btn btn-outline-primary ${filter === "3" ? "active" : ""}`}
            onClick={() => setFilter("3")}
          >
            3
          </button>
        </div>
      </div>
      <ul>
        {filteredData.map(({ item, index }) => (
          <li key={index}>
            {item === null ? (
              <span>Wird geladen...</span>
            ) : (
              <div dangerouslySetInnerHTML={{__html: item.html}}
                   ref={el => {
                     // Search for Button an assign ref
                     if (el) {
                        buttonRefs.current[index] = el.querySelector('.btn-favorite');
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
react_root.render(<Listing items={root.getAttribute("data-listing-items")}/>);
