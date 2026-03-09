const { app, BrowserWindow } = require("electron");

function createWindow() {
  const win = new BrowserWindow({
    width: 400,
    height: 600,
    transparent: true,
    frame: false
  });

  win.loadFile("overlay.html");
}

app.whenReady().then(createWindow);