function baseName(path, extension = true) {
  var base = path.substring(path.lastIndexOf("/") + 1);
  if (!extension) {
    if (base.lastIndexOf(".") !== -1) {
      base = base.substring(0, base.lastIndexOf("."));
    }
  }
  return base;
}

function dataUrlToFile(dataUrl, fileName) {
  const arr = dataUrl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n) {
    u8arr[n - 1] = bstr.charCodeAt(n - 1);
    n -= 1; // to make eslint happy
  }
  return new File([u8arr], fileName, { type: mime, lastModified: new Date() });
}

export default {
  baseName,
  dataUrlToFile,
};
