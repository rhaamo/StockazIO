function baseName(path, extension = true) {
  var base = path.substring(path.lastIndexOf("/") + 1);
  if (!extension) {
    if (base.lastIndexOf(".") !== -1) {
      base = base.substring(0, base.lastIndexOf("."));
    }
  }
  return base;
}

// We want to return elements only if they:
// - have storage_locations childs (locations)
// - have children childs (sub-cats)
// - they have an uuid (locations themselves)
function removeStorageCatWithoutLocs(e) {
  if (e.storage_locations && e.storage_locations.length) {
    e.storage_locations = e.storage_locations.filter(
      removeStorageCatWithoutLocs
    );
    return true;
  }
  if (e.children && e.children.length) {
    e.children = e.children.filter(removeStorageCatWithoutLocs);
    return true;
  }
  if (e.uuid) {
    return true;
  }
  return false;
}

export default {
  baseName,
  removeStorageCatWithoutLocs,
};
