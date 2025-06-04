import "bootstrap";
import React, {useState, useRef, useEffect} from "react";
import {createRoot} from "react-dom/client";
import "./base.scss";

const Listing = ({items}) => {
  const [data, setData] = useState([]);
  const buttonRefs = useRef({});
  const eventHandlers = useRef({});

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

  // Add event listener to all buttons
  useEffect(() => {
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

  return (
    <div>
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
