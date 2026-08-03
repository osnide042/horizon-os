import QtQuick
import org.kde.plasma.plasmoid

WallpaperItem {
    id: root
    property real phase: 0

    Canvas {
        id: canvas
        anchors.fill: parent
        renderStrategy: Canvas.Threaded
        onPaint: {
            var c = getContext("2d")
            var w = width, h = height
            c.clearRect(0, 0, w, h)
            var bg = c.createLinearGradient(0, 0, w, h)
            bg.addColorStop(0, "#071b42")
            bg.addColorStop(0.48, "#070a19")
            bg.addColorStop(1, "#270b49")
            c.fillStyle = bg; c.fillRect(0, 0, w, h)

            function blob(x, y, r, inner) {
                var g = c.createRadialGradient(x, y, 0, x, y, r)
                g.addColorStop(0, inner); g.addColorStop(1, "rgba(20,20,70,0)")
                c.fillStyle = g; c.fillRect(x-r, y-r, r*2, r*2)
            }
            blob(w*(0.12 + 0.08*Math.sin(root.phase)), h*(0.18 + 0.10*Math.cos(root.phase*.7)), w*.48, "rgba(36,143,255,.72)")
            blob(w*(0.86 + 0.07*Math.cos(root.phase*.8)), h*(0.80 + 0.08*Math.sin(root.phase*.9)), w*.48, "rgba(139,70,255,.68)")
            blob(w*(0.55 + 0.10*Math.sin(root.phase*.55)), h*(0.38 + 0.06*Math.cos(root.phase*.6)), w*.22, "rgba(36,185,255,.22)")

            c.strokeStyle = "rgba(255,255,255,.035)"; c.lineWidth = 1
            for (var x=0; x<w; x+=w/8) { c.beginPath(); c.moveTo(x,0); c.lineTo(x,h); c.stroke() }
            for (var y=0; y<h; y+=h/6) { c.beginPath(); c.moveTo(0,y); c.lineTo(w,y); c.stroke() }

            c.textAlign = "center"; c.fillStyle = "rgba(255,255,255,.96)"
            c.font = "800 " + Math.max(48,w*.052) + "px Noto Sans"
            c.fillText("HORIZON", w/2, h*.48)
            c.fillStyle = "rgba(123,201,255,.9)"; c.font = "600 " + Math.max(12,w*.012) + "px Noto Sans"
            c.fillText("D E S K T O P", w/2, h*.53)
        }
    }

    NumberAnimation on phase {
        from: 0; to: Math.PI * 2; duration: 24000
        loops: Animation.Infinite; running: true
    }
    onPhaseChanged: canvas.requestPaint()
}
