/**
 * Bang Motion After Effects Builder: Explainer The Great Dying (70-Second English Document Edition)
 * Automatically builds composition, camera rig, assets, layers, text, and keyframes in Adobe After Effects.
 * 
 * Usage:
 * In Adobe After Effects: File -> Scripts -> Run Script File... -> Select this file.
 */

(function buildGreatDyingExplainer70s() {
    app.beginUndoGroup("Build Bang Motion Great Dying 70s");

    var compWidth = 1080;
    var compHeight = 1920;
    var pixelAspect = 1.0;
    var duration = 70.0;
    var frameRate = 30.0;

    // 1. Create Master Composition
    var compName = "EXPLAINER_THE_GREAT_DYING_70S";
    var comp = app.project.items.addComp(compName, compWidth, compHeight, pixelAspect, duration, frameRate);

    var scriptFile = new File($.fileName);
    var projectFolder = scriptFile.parent;
    var assetsImagesFolder = new Folder(projectFolder.fsName + "/assets/episode2_great_dying/images");
    var assetsAudioFolder = new Folder(projectFolder.fsName + "/assets/episode2_great_dying/audio");

    // 2. Add Off-White Museum Archival Background Solid
    var bgSolid = comp.layers.addSolid([0.984, 0.988, 0.992], "BG_ARCHIVAL_PAPER", compWidth, compHeight, pixelAspect, duration);
    bgSolid.moveToEnd();

    // 3. Create Camera Null Controller
    var camNull = comp.layers.addNull();
    camNull.name = "CAM";
    camNull.property("Transform").property("Anchor Point").setValue([compWidth / 2, compHeight / 2]);
    camNull.property("Transform").property("Position").setValue([compWidth / 2, compHeight / 2]);

    // Animate CAM Position across the 6 stages (spaced 2000px horizontally)
    var camPos = camNull.property("Transform").property("Position");
    
    // Stage 1 (0.0s - 10.4s | Xc = 540)
    camPos.setValueAtTime(0.0, [540, 960]);
    camPos.setValueAtTime(9.3, [540, 960]);
    
    // Stage 2 (10.4s - 21.4s | Xc = 2540)
    camPos.setValueAtTime(10.4, [-1460, 960]);
    camPos.setValueAtTime(20.3, [-1460, 960]);
    
    // Stage 3 (21.4s - 32.3s | Xc = 4540)
    camPos.setValueAtTime(21.4, [-3460, 960]);
    camPos.setValueAtTime(32.1, [-3460, 960]);
    
    // Stage 4 (33.2s - 43.0s | Xc = 6540)
    camPos.setValueAtTime(33.2, [-5460, 960]);
    camPos.setValueAtTime(42.8, [-5460, 960]);
    
    // Stage 5 (44.0s - 53.8s | Xc = 8540)
    camPos.setValueAtTime(44.0, [-7460, 960]);
    camPos.setValueAtTime(53.6, [-7460, 960]);
    
    // Stage 6 & Outro (54.8s - 70.0s | Xc = 10540)
    camPos.setValueAtTime(54.8, [-9460, 960]);
    camPos.setValueAtTime(70.0, [-9460, 960]);

    // Apply smooth Ease to CAM keyframes
    var easeIn = new KeyframeEase(0.0, 75.0);
    var easeOut = new KeyframeEase(0.0, 75.0);
    for (var k = 1; k <= camPos.numKeys; k++) {
        camPos.setTemporalEaseAtKey(k, [easeIn, easeIn, easeIn], [easeOut, easeOut, easeOut]);
    }

    // 4. Import and Place Audio Track
    var audioFile = new File(assetsAudioFolder.fsName + "/vo_great_dying.wav");
    if (audioFile.exists) {
        var audioItem = app.project.importFile(new ImportOptions(audioFile));
        var audioLayer = comp.layers.add(audioItem);
        audioLayer.name = "VO_KOKORO_ENGLISH_70S";
        audioLayer.audioEnabled = true;
    }

    // Helper: Import image and place with parent to CAM
    function addCatalogSprite(fileName, layerName, stageOffset, xOffset, yPos, targetScale, inPoint, outPoint) {
        var f = new File(assetsImagesFolder.fsName + "/" + fileName);
        if (!f.exists) return null;
        var item = app.project.importFile(new ImportOptions(f));
        var layer = comp.layers.add(item);
        layer.name = layerName;
        layer.parent = camNull;
        
        var xPos = (compWidth / 2) + stageOffset + xOffset;
        layer.property("Transform").property("Position").setValue([xPos, yPos]);
        layer.property("Transform").property("Scale").setValue([targetScale, targetScale]);
        
        var op = layer.property("Transform").property("Opacity");
        op.setValueAtTime(inPoint, 0);
        op.setValueAtTime(inPoint + 0.45, 100);

        var sc = layer.property("Transform").property("Scale");
        sc.setValueAtTime(inPoint, [targetScale * 0.85, targetScale * 0.85]);
        sc.setValueAtTime(inPoint + 0.6, [targetScale, targetScale]);
        
        if (outPoint) {
            layer.outPoint = outPoint;
        }
        return layer;
    }

    // 5. Build Scene Assets parented to CAM
    // Scene 1: The Permian Paradise (stageOffset: 0)
    addCatalogSprite("permian_jungle.png", "CARD_PERMIAN_JUNGLE", 0, -160, 580, 52, 0.5, 10.4);
    addCatalogSprite("gorgonopsian_skull.png", "CUT_GORGONOPSIAN_SKULL", 0, 230, 585, 41, 0.7, 10.4);
    addCatalogSprite("trilobite_fossil.png", "CUT_TRILOBITE_FOSSIL", 0, -320, 695, 21, 1.0, 10.4);

    // Scene 2: The Siberian Traps Inferno (stageOffset: 2000)
    addCatalogSprite("mantle_plume.png", "CARD_MANTLE_PLUME", 2000, -160, 580, 52, 10.8, 21.4);
    addCatalogSprite("siberian_basalt_flood.png", "CUT_BASALT_FLOOD", 2000, 230, 585, 41, 11.0, 21.4);
    addCatalogSprite("basalt_rock_specimen.png", "CUT_BASALT_ROCK", 2000, -320, 695, 21, 11.3, 21.4);

    // Scene 3: Coal Fires & Acid Rain (stageOffset: 4000)
    addCatalogSprite("acid_rain_forest.png", "CARD_ACID_FOREST", 4000, -160, 580, 52, 21.8, 32.3);
    addCatalogSprite("toxic_smoke_plume.png", "CUT_SMOKE_PLUME", 4000, 230, 585, 41, 22.0, 32.3);

    // Scene 4: The Purple Dying Oceans (stageOffset: 6000)
    addCatalogSprite("purple_toxic_ocean.png", "CARD_PURPLE_OCEAN", 6000, -160, 580, 52, 33.6, 43.0);
    addCatalogSprite("anoxic_water_sample.png", "CUT_WATER_SAMPLE", 6000, 220, 585, 38, 33.8, 43.0);

    // Scene 5: The Fungal Spike & Total Collapse (stageOffset: 8000)
    addCatalogSprite("barren_earth_landscape.png", "CARD_BARREN_EARTH", 8000, -160, 580, 52, 44.4, 53.8);
    addCatalogSprite("fungal_spike_fossil.png", "CUT_FUNGAL_SPIKE", 8000, 230, 585, 41, 44.6, 53.8);

    // Scene 6: The Lonely Survivor & Dawn of Dinosaurs (stageOffset: 10000)
    addCatalogSprite("lystrosaurus_fossil.png", "CUT_LYSTROSAURUS", 10000, -210, 580, 43, 55.2, 64.6);
    addCatalogSprite("early_dino_tracks.png", "CUT_DINO_TRACKS", 10000, 225, 590, 40, 55.5, 64.6);

    app.endUndoGroup();
    alert("Bang Motion Episode 2: The Great Dying (70s) built successfully in After Effects!");
})();
