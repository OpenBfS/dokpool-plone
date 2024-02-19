export function getURLParam(name) {
  var regex = "[?&]" + name + "=([^&]*)";
  var query = location.search;
  if ((name = new RegExp(regex).exec(query))) return name[1];
}
