import QtQuick
import Quickshell
import qs.Commons

// Loads one plugin entry point (or, with no WIDGET, a stock bar strip) in an ordinary window,
// offscreen. Prints every string it drew as PREVIEW_TEXT lines and, for visual entries, saves
// a picture. Nothing is drawn on a display: QT_QPA_PLATFORM=offscreen.
ShellRoot {
  FakeBar { id: fakeBar }
  FloatingWindow {
    id: win
    implicitWidth: Number(Quickshell.env("PREVIEW_W") || 420); implicitHeight: 34
    Rectangle {
      id: frame; anchors.fill: parent; color: Color.bar.background
      Row {
        anchors.centerIn: parent; spacing: 14
        Loader { active: Quickshell.env("STRIP") === "1"; source: "file:///usr/share/omarchy/shell/plugins/panels/clock/BarWidget.qml"
                 onLoaded: { item.bar = fakeBar; item.settings = { "format": "ddd HH:mm" } } }
        Loader {
          id: loader
          active: (Quickshell.env("WIDGET") || "") !== ""
          source: Quickshell.env("WIDGET") || ""
          onStatusChanged: if (status === Loader.Error) console.warn("PREVIEW_LOAD_ERROR " + source)
          onLoaded: {
            if (item && ("bar" in item)) item.bar = fakeBar
            if (item && ("settings" in item)) item.settings = JSON.parse(Quickshell.env("SETTINGS") || "{}")
            if (item && ("moduleName" in item)) item.moduleName = Quickshell.env("MODULE") || ""
          }
        }
        Row { visible: Quickshell.env("STRIP") === "1"; spacing: 4; anchors.verticalCenter: parent.verticalCenter
          Repeater { model: [Color.accent, Color.foreground, Color.muted, Color.urgent]
            Rectangle { width: 14; height: 14; radius: 3; color: modelData } } }
      }
    }
    function texts(it, out) {
      if (!it) return out
      if (it.text !== undefined && it.visible !== false && String(it.text).trim() !== "") out.push(String(it.text))
      var kids = it.children || []
      for (var i = 0; i < kids.length; i++) texts(kids[i], out)
      return out
    }
    Timer { interval: Number(Quickshell.env("WAIT_MS") || 2500); running: true
      onTriggered: {
        var t = win.texts(frame, [])
        for (var i = 0; i < t.length; i++) console.info("PREVIEW_TEXT " + t[i].replace(/\n/g, " / "))
        var shot = Quickshell.env("SHOT") || ""
        if (shot) frame.grabToImage(function(r) { r.saveToFile(shot); Qt.quit() })
        else Qt.quit()
      }
    }
  }
}
