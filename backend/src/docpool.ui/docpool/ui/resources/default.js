import "bootstrap";
import React, { useState } from "react";
import { createRoot } from "react-dom/client";

const fetchItem = async (item, itemHTML, setItemHTML) => {
  const response = await fetch("http://localhost:8080/Plone/listing-item?title=" + item);
  let html_body = response.body;
  setItemHTML(html_body);
};

const Listing = ({ items }) => {
  const [itemHTML, setItemHTML] = useState({});

  items = JSON.parse(items);
  for (let item in items) {
    console.log(item);
    fetchItem(item, itemHTML, setItemHTML);
  }

  return (
    <ul>
      {items.map((item) => {
        <li key={item} dangerouslySetInnerHTML={{ __html: itemHTML[item] }}></li>;
      })}
    </ul>
  );
};
const root = document.getElementById("docpool-listing");
const react_root = createRoot(root);
react_root.render(<Listing items={root.getAttribute("data-listing-items")} />);
