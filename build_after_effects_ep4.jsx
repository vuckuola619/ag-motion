/**
 * Adobe After Effects Automation Script for Episode 4:
 * "THE DAY THE DINOSAURS DIED: Minute-by-Minute of the Chicxulub Impact"
 *
 * Usage:
 * In After Effects: File -> Scripts -> Run Script File... -> Select build_after_effects_ep4.jsx
 */

(function buildChicxulubComp() {
    app.beginUndoGroup("Build Episode 4: Chicxulub Impact Comp");

    var compWidth = 1080;
    var compHeight = 1920;
    var pixelAspect = 1.0;
    var duration = 70.0;
    var frameRate = 30.0;
    var compName = "EPISODE_04_CHICXULUB_IMPACT_MASTER";

    // 1. Create Master 9:16 Vertical Composition
    var comp = app.project.items.addComp(compName, compWidth, compHeight, pixelAspect, duration, frameRate);

    var scriptFile = new File($.fileName);
    var projectFolder = scriptFile.parent;
    var assetsImagesFolder = new Folder(projectFolder.fsName + "/assets/episode4_chicxulub/images");
    var assetsAudioFolder = new Folder(projectFolder.fsName + "/assets/episode4_chicxulub/audio");

    // 2. Add Off-White Museum Archival Background Solid
    var bgSolid = comp.layers.addSolid([0.984, 0.988, 0.992], "BG_ARCHIVAL_PAPER", compWidth, compHeight, pixelAspect, duration);
    bgSolid.moveToEnd();

    // 3. Create Camera Null Controller
    var camNull = comp.layers.addNull();
    camNull.name = "CAM";
    camNull.property("Transform").property("Anchor Point").setValue([compWidth / 2, compHeight / 2]);
    camNull.property("Transform").property("Position").setValue([compWidth / 2, compHeight / 2]);

    // 4. Import Master Audio Track
    var audioFile = new File(assetsAudioFolder.fsName + "/vo_chicxulub_cinematic.wav");
    if (audioFile.exists) {
        var audioItem = app.project.importFile(new ImportOptions(audioFile));
        var audioLayer = comp.layers.add(audioItem);
        audioLayer.name = "AUDIO_MASTER_VO_SFX";
        audioLayer.moveToEnd();
    }

    // 5. Add Scene Chapter Markers
    var sceneBeats = [
        { time: 0.0,  name: "SCENE 1: T-Minus 10s · The Impactor Approaches" },
        { time: 10.4, name: "SCENE 2: Minute 0 · Ground Zero Impact" },
        { time: 21.4, name: "SCENE 3: Minute 5 · The Thermal Radiation Pulse" },
        { time: 32.3, name: "SCENE 4: Hour 1 · Molten Glass & Megatsunamis" },
        { time: 43.0, name: "SCENE 5: Hour 24 · The Nuclear Ash Winter" },
        { time: 53.8, name: "SCENE 6: Day 1000 · The Mammalian Dawn" },
        { time: 64.8, name: "SCENE 7: Epilogue Outro Resolution" }
    ];

    for (var i = 0; i < sceneBeats.length; i++) {
        var markerVal = new MarkerValue(sceneBeats[i].name);
        comp.markerProperty.setValueAtTime(sceneBeats[i].time, markerVal);
    }

    app.endUndoGroup();
    alert("Episode 4: Chicxulub Impact composition built successfully!\nResolution: 1080x1920 @ 30fps (70.0s)");
})();
