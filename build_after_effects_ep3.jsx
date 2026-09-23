/**
 * Adobe After Effects Automation Script for Episode 3:
 * "THE 2-MILLION-YEAR RAINSTORM: The Carnian Pluvial Event"
 *
 * Usage:
 * In After Effects: File -> Scripts -> Run Script File... -> Select build_after_effects_ep3.jsx
 */

(function buildCarnianPluvialComp() {
    app.beginUndoGroup("Build Episode 3: Carnian Pluvial Comp");

    var compWidth = 1080;
    var compHeight = 1920;
    var pixelAspect = 1.0;
    var duration = 70.0;
    var frameRate = 30.0;
    var compName = "EPISODE_03_CARNIAN_PLUVIAL_MASTER";

    // 1. Create Master 9:16 Vertical Composition
    var comp = app.project.items.addComp(compName, compWidth, compHeight, pixelAspect, duration, frameRate);

    var scriptFile = new File($.fileName);
    var projectFolder = scriptFile.parent;
    var assetsImagesFolder = new Folder(projectFolder.fsName + "/assets/episode3_carnian_pluvial/images");
    var assetsAudioFolder = new Folder(projectFolder.fsName + "/assets/episode3_carnian_pluvial/audio");

    // 2. Add Off-White Museum Archival Background Solid
    var bgSolid = comp.layers.addSolid([0.984, 0.988, 0.992], "BG_ARCHIVAL_PAPER", compWidth, compHeight, pixelAspect, duration);
    bgSolid.moveToEnd();

    // 3. Create Camera Null Controller
    var camNull = comp.layers.addNull();
    camNull.name = "CAM";
    camNull.property("Transform").property("Anchor Point").setValue([compWidth / 2, compHeight / 2]);
    camNull.property("Transform").property("Position").setValue([compWidth / 2, compHeight / 2]);

    // 4. Import Master Audio Track
    var audioFile = new File(assetsAudioFolder.fsName + "/vo_carnian_pluvial_cinematic.wav");
    if (audioFile.exists) {
        var audioItem = app.project.importFile(new ImportOptions(audioFile));
        var audioLayer = comp.layers.add(audioItem);
        audioLayer.name = "AUDIO_MASTER_VO_SFX";
        audioLayer.moveToEnd();
    }

    // 5. Add Scene Chapter Markers
    var sceneBeats = [
        { time: 0.0,  name: "SCENE 1: The Arid Pangea Dustbowl" },
        { time: 10.4, name: "SCENE 2: Wrangellia Oceanic Volcano" },
        { time: 21.4, name: "SCENE 3: The 2-Million-Year Deluge" },
        { time: 32.3, name: "SCENE 4: The Amber Spike & Conifer Swamps" },
        { time: 43.0, name: "SCENE 5: The Carnian Extinction" },
        { time: 53.8, name: "SCENE 6: The Dawn of Dinosaurs" },
        { time: 64.8, name: "SCENE 7: Resolution Outro Card" }
    ];

    for (var i = 0; i < sceneBeats.length; i++) {
        var markerVal = new MarkerValue(sceneBeats[i].name);
        comp.markerProperty.setValueAtTime(sceneBeats[i].time, markerVal);
    }

    app.endUndoGroup();
    alert("Episode 3: Carnian Pluvial Event composition built successfully!\nResolution: 1080x1920 @ 30fps (70.0s)");
})();
