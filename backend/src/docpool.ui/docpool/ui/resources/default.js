import "bootstrap";
import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";

const Listing = ({ items }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    let json_items = JSON.parse(items);
    const fetchData = async () => {
      const urls = json_items.map((item) => `http://localhost:8080/Plone/listing-item?title=${item}`);
      console.log(urls);
      try {
        const responses = await Promise.all(urls.map((url) => fetch(url)));
        const html = await Promise.all(responses.map((res) => res.text()));
        console.log(html);
        setData(html);
      } catch (error) {
        console.error("Fehler beim Laden der Daten", error);
      }
    };

    fetchData();
  }, [items]);

  return (
    <ul>
      {data.map((item, index) => (
        <li key={index} dangerouslySetInnerHTML={{ __html: item }}></li>
      ))}
    </ul>
  );
};

const root = document.getElementById("docpool-listing");
const react_root = createRoot(root);
react_root.render(<Listing items={root.getAttribute("data-listing-items")} />);
