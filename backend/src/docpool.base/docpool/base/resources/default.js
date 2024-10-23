// docpool.base js/scss entry

import("./styles.scss");

// Fixes much margin around inner iframe
const iframe = document.getElementById("dpdocument-dview-commenting");
if (iframe) {
  iframe.onload = function () {
    const iframeDocument = iframe.contentDocument || iframe.contentWindow.document;

    const style = document.createElement("style");
    style.innerHTML = `
      body.plone-toolbar-left {
        padding-left: 0 !important;
      }
      body > article.bfs_popup {
        margin: 0 !important;
      }
    `;

    // Das Style-Element zum head des iframes hinzufügen
    iframeDocument.head.appendChild(style);
  };
}
