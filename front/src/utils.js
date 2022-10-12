function baseName(path, extension = true) {
  var base = path.substring(path.lastIndexOf("/") + 1);
  if (!extension) {
    if (base.lastIndexOf(".") !== -1) {
      base = base.substring(0, base.lastIndexOf("."));
    }
  }
  return base;
}

export default {
  baseName,
};
