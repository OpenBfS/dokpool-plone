import "bootstrap";
import React from "react";
import { createRoot } from "react-dom/client";

const Listing = () => {
  console.log("test");
  return <span class="badge text-bg-danger">I am your father</span>;
};

const root = createRoot(document.getElementById("docpool-listing"));
root.render(<Listing />);
