import "bootstrap";
import React from "react";
import { render } from "react-dom";

const Listing = () => {
  console.log("test");
  return <div>test</div>;
};

const el = document.getElementById("docpool-listing");
console.log(el);
render(<Listing />, el);
