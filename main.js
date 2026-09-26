// Sine si Sosele - fereastra desktop (Electron) pentru versiunea de Steam
const { app, BrowserWindow, Menu, shell } = require('electron');
const path = require('path');

// Ajuta overlay-ul Steam (Shift+Tab) sa apara peste joc pe Windows
app.commandLine.appendSwitch('in-process-gpu');
app.commandLine.appendSwitch('disable-direct-composition');

function createWindow() {
  const win = new BrowserWindow({
    width: 1600,
    height: 900,
    minWidth: 1024,
    minHeight: 640,
    title: 'Sine si Sosele',
    backgroundColor: '#CFD4C8',
    show: false,
    autoHideMenuBar: true,
    webPreferences: { contextIsolation: true, sandbox: true }
  });
  Menu.setApplicationMenu(null);
  win.once('ready-to-show', () => { win.maximize(); win.show(); });
  win.loadFile(path.join(__dirname, 'game', 'index.html'));
  // linkurile externe se deschid in browser, nu in joc
  win.webContents.setWindowOpenHandler(({ url }) => { shell.openExternal(url); return { action: 'deny' }; });
  // F11 = ecran complet
  win.webContents.on('before-input-event', (e, input) => {
    if (input.type === 'keyDown' && input.key === 'F11') { win.setFullScreen(!win.isFullScreen()); e.preventDefault(); }
  });
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());
