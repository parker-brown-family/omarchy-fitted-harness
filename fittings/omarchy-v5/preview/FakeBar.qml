import QtQuick
import qs.Commons

// A stand-in for the bar host Omarchy hands every bar widget, carrying the members stock widgets
// use, in the current theme's colours. run() is recorded, never executed: a preview must not act.
QtObject {
  property string position: "top"
  property bool vertical: false
  property bool transparent: false
  property bool barHidden: false
  property bool active: true
  property real x: 0
  property int sizeHorizontal: Style.bar.sizeHorizontal
  property int sizeVertical: Style.bar.sizeVertical !== undefined ? Style.bar.sizeVertical : Style.bar.sizeHorizontal
  property int barSize: sizeHorizontal
  property string fontFamily: Style.font.family
  property color foreground: Color.bar.text
  property color barForeground: Color.bar.text
  property color text: Color.bar.text
  property color background: Color.bar.background
  property color urgent: Color.bar.active
  property bool foregroundAnimationEnabled: true
  property bool centerHoverRevealSuppressed: false
  property bool centerSectionRevealHeld: false
  property var shell: null
  property var layout: ({})
  property var layoutConfig: ({})
  property var activePopout: null
  property var clickTargets: []
  function run(command) { console.info("PREVIEW_RUN " + command) }
  function showTooltip(target, text) {}
  function hideTooltip(target) {}
  function requestPopout(owner) { return true }
  function releasePopout(owner) {}
  function switchPanelFrom(owner, direction) { return false }
  function moduleWidgets(pluginId) { return [] }
  function targetBelongsToWindow(target, window) { return false }
  function setCenterHoverRevealSuppressed(value) { centerHoverRevealSuppressed = value }
  function shellQuote(s) { return "'" + String(s).replace(/'/g, "'\\''") + "'" }
}
