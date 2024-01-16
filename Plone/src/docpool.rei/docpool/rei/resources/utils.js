// Copy from mockup as an import does not work
// https://github.com/plone/mockup/blob/master/src/core/utils.js

var parseBodyTag = function (txt) {
  return $(
    /<body[^>]*>[^]*<\/body>/im
      .exec(txt)[0]
      .replace("<body", "<div")
      .replace("</body>", "</div>"),
  )
    .eq(0)
    .html();
};
export default parseBodyTag;
