function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Pioneer Trail')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
