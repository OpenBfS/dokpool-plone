import "bootstrap";
import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import "./base.scss";

const Listing = ({ items }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    let json_items = JSON.parse(items);
    const fetchData = async () => {
      const urls = json_items.map((item) => `http://localhost:8080/Plone/listing-item?title=${item}`);
      console.log(urls);

      // Empty the data array
      setData(new Array(urls.length).fill(null));

      // Process each URL
      urls.forEach(async (url, index) => {
        try {
          const response = await fetch(url);
          const html = await response.text();
          console.log(`Loaded item ${index}:`, html);

          // Update items in the array
          setData(prevData => {
            const newData = [...prevData];
            newData[index] = html;
            return newData;
          });
        } catch (error) {
          console.error(`Error on URL ${url}`, error);
        }
      });
    };

    fetchData();
  }, [items]);

  return (
    <ul>
      {data.map((item, index) => (
        <li key={index}>
          {item === null ? (
            <span>Wird geladen...</span>
          ) : (
            <div dangerouslySetInnerHTML={{ __html: item }}></div>
          )}
        </li>
      ))}
    </ul>
  );
};

const root = document.getElementById("docpool-listing");
const react_root = createRoot(root);
react_root.render(<Listing items={root.getAttribute("data-listing-items")} />);
