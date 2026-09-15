/**
 * Bang Motion After Effects Builder: Explainer The Extinction of Dinosaurs (60-Second English White Catalog Edition)
 * Automatically builds composition, camera rig, assets, layers, text, and keyframes in Adobe After Effects.
 * 
 * Usage:
 * In Adobe After Effects: File -> Scripts -> Run Script File... -> Select this file.
 */

(function buildDinosaurExplainer60s() {
    app.beginUndoGroup("Build Bang Motion Dinosaur Explainer 60s");

    var compWidth = 1080;
    var compHeight = 1920;
    var pixelAspect = 1.0;
    var duration = 60.0;
    var frameRate = 30.0;

    // 1. Create Master Composition
    var compName = "EXPLAINER_EXTINCTION_OF_DINOSAURS_60S";
    var comp = app.project.items.addComp(compName, compWidth, compHeight, pixelAspect, duration, frameRate);

    var scriptFile = new File($.fileName);
    var projectFolder = scriptFile.parent;
    var assetsImagesFolder = new Folder(projectFolder.fsName + "/assets/images");
    var assetsAudioFolder = new Folder(projectFolder.fsName + "/assets/audio");
    var assetsVideoFolder = new Folder(projectFolder.fsName + "/assets/video");

    // 2. Add White Background Solid
    var bgSolid = comp.layers.addSolid([1.0, 1.0, 1.0], "BG_WHITE_PAPER", compWidth, compHeight, pixelAspect, duration);
    bgSolid.moveToEnd();

    // 3. Create Camera Null Controller
    var camNull = comp.layers.addNull();
    camNull.name = "CAM";
    camNull.property("Transform").property("Anchor Point").setValue([compWidth / 2, compHeight / 2]);
    camNull.property("Transform").property("Position").setValue([compWidth / 2, compHeight / 2]);

    // Animate CAM Position across the 6 stages (spaced 2000px horizontally)
    var camPos = camNull.property("Transform").property("Position");
    // Stage 1 (0.0s - 10.0s)
    camPos.setValueAtTime(0.0, [540, 960]);
    camPos.setValueAtTime(9.3, [540, 960]);
    // Stage 2 (10.0s - 20.0s)
    camPos.setValueAtTime(10.15, [-1460, 960]);
    camPos.setValueAtTime(19.3, [-1460, 960]);
    // Stage 3 (20.0s - 30.0s)
    camPos.setValueAtTime(20.15, [-3460, 960]);
    camPos.setValueAtTime(29.3, [-3460, 960]);
    // Stage 4 (30.0s - 40.0s)
    camPos.setValueAtTime(30.15, [-5460, 960]);
    camPos.setValueAtTime(39.3, [-5460, 960]);
    // Stage 5 (40.0s - 50.0s)
    camPos.setValueAtTime(40.15, [-7460, 960]);
    camPos.setValueAtTime(49.3, [-7460, 960]);
    // Stage 6 (50.0s - 60.0s)
    camPos.setValueAtTime(50.15, [-9460, 960]);
    camPos.setValueAtTime(60.0, [-9460, 960]);

    // Apply smooth Ease to CAM keyframes
    var easeIn = new KeyframeEase(0.0, 75.0);
    var easeOut = new KeyframeEase(0.0, 75.0);
    for (var k = 1; k <= camPos.numKeys; k++) {
        camPos.setTemporalEaseAtKey(k, [easeIn, easeIn, easeIn], [easeOut, easeOut, easeOut]);
    }

    // 4. Import and Place Audio Track
    var audioFile = new File(assetsAudioFolder.fsName + "/vo_dinosaurus.wav");
    if (audioFile.exists) {
        var audioItem = app.project.importFile(new ImportOptions(audioFile));
        var audioLayer = comp.layers.add(audioItem);
        audioLayer.name = "VO_KOKORO_ENGLISH_60S";
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

    // Helper: Add text card
    function addTextCard(titleText, stageOffset, yPos, fontSize, inPoint, outPoint) {
        var textLayer = comp.layers.addText(titleText);
        textLayer.parent = camNull;
        var textProp = textLayer.property("Source Text");
        var textDoc = textProp.value;
        textDoc.fontSize = fontSize;
        textDoc.fillColor = [0.07, 0.09, 0.16];
        textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
        textProp.setValue(textDoc);

        var xPos = (compWidth / 2) + stageOffset;
        textLayer.property("Transform").property("Position").setValue([xPos, yPos]);
        
        var op = textLayer.property("Transform").property("Opacity");
        op.setValueAtTime(inPoint, 0);
        op.setValueAtTime(inPoint + 0.35, 100);
        
        if (outPoint) {
            textLayer.outPoint = outPoint;
        }
        return textLayer;
    }

    // Stage 1: The Age of Dinosaurs (Offset: 0)
    addCatalogSprite("trex_fossil.png", "SPRITE_TREX_FOSSIL", 0, 0, 560, 75, 0.5, 10.0);
    addCatalogSprite("sauropod_fossil.png", "SPRITE_SAUROPOD", 0, 260, 710, 42, 1.2, 10.0);
    addTextCard("EXTINCTION ARCHIVE // DOSSIER #01", 0, 120, 20, 0.2, 10.0);
    addTextCard("165 MILLION YEARS OF REIGN", 0, 890, 26, 1.9, 10.0);
    addTextCard("66 million years ago, dinosaurs were the absolute rulers of Earth.", 0, 1050, 44, 0.8, 10.0);

    // Stage 2: The Chicxulub Impactor (Offset: 2000px)
    addCatalogSprite("asteroid_entry_realistic.png", "SPRITE_ASTEROID_ENTRY", 2000, -140, 580, 55, 10.4, 20.0);
    addCatalogSprite("meteorite_chondrite.png", "SPRITE_CHONDRITE", 2000, 240, 600, 48, 11.1, 20.0);
    addTextCard("EXTINCTION ARCHIVE // DOSSIER #02", 2000, 200, 20, 10.1, 20.0);
    addTextCard("VELOCITY: 45,000 MPH", 2000, 920, 26, 11.9, 20.0);
    addTextCard("A massive 10-kilometer asteroid plunged from space toward Earth.", 2000, 1050, 44, 10.7, 20.0);

    // Stage 3: Cataclysmic Impact & Megatsunami (Offset: 4000px)
    addCatalogSprite("megatsunami_wave_realistic.png", "SPRITE_MEGATSUNAMI", 4000, -140, 580, 55, 20.4, 30.0);
    addCatalogSprite("chicxulub_crater_aerial.png", "SPRITE_CRATER_AERIAL", 4000, 240, 600, 45, 21.1, 30.0);
    addTextCard("EXTINCTION ARCHIVE // DOSSIER #03", 4000, 200, 20, 20.1, 30.0);
    addTextCard("TSUNAMI SURGE: 1,000+ FEET", 4000, 920, 26, 21.9, 30.0);
    addTextCard("The impact detonated with unimaginable fury, unleashing megatsunamis.", 4000, 1050, 44, 20.7, 30.0);

    // Stage 4: Deccan Traps Supervolcanoes (Offset: 6000px)
    addCatalogSprite("deccan_volcano.png", "SPRITE_VOLCANO", 6000, -140, 530, 75, 30.4, 40.0);
    addCatalogSprite("firestorm_sky.png", "SPRITE_FIRESTORM", 6000, 260, 490, 46, 31.1, 40.0);
    addTextCard("EXTINCTION ARCHIVE // DOSSIER #04", 6000, 120, 20, 30.1, 40.0);
    addTextCard("ERUPTION: 240,000 CU MILES", 6000, 890, 26, 31.9, 40.0);
    addTextCard("Shockwaves fractured Earth's mantle, triggering supervolcanoes in Deccan.", 6000, 1050, 44, 30.7, 40.0);

    // Stage 5: Nuclear Winter & Biosphere Collapse (Offset: 8000px)
    addCatalogSprite("sun_blackout.png", "SPRITE_SUN_BLACKOUT", 8000, -180, 540, 52, 40.4, 50.0);
    addCatalogSprite("fern_fossil.png", "SPRITE_FERN_FOSSIL", 8000, 180, 550, 52, 41.1, 50.0);
    addTextCard("EXTINCTION ARCHIVE // DOSSIER #05", 8000, 120, 20, 40.1, 50.0);
    addTextCard("SUN BLOCKED FOR 10+ YEARS", 8000, 890, 26, 41.9, 50.0);
    addTextCard("A dense shroud of soot choked the globe. Photosynthesis ceased.", 8000, 1050, 44, 40.7, 50.0);

    // Stage 6: The Iridium Boundary & Dawn of Mammals (Offset: 10000px)
    addCatalogSprite("iridium_layer.png", "SPRITE_IRIDIUM_CORE", 10000, -180, 540, 52, 50.4, 55.4);
    addCatalogSprite("mammal_survivor.png", "SPRITE_MAMMAL", 10000, 180, 550, 52, 51.1, 55.4);
    addTextCard("EXTINCTION ARCHIVE // FINAL DOSSIER", 10000, 120, 20, 50.1, 55.4);
    addTextCard("75% OF ALL SPECIES EXTINCT", 10000, 890, 26, 51.8, 55.4);
    addTextCard("Dinosaurs perished forever. The dawn of mammals had begun.", 10000, 1050, 44, 50.7, 55.4);

    // Outro Resolution Dossier Card (55.6s - 60.0s)
    addTextCard("THE LEGACY OF 66 MILLION YEARS", 10000, 850, 48, 55.6, 60.0);
    addTextCard("Without Chicxulub, mammals would never have inherited Earth.", 10000, 940, 26, 55.8, 60.0);
    addTextCard("What if the asteroid had missed? Comment below!", 10000, 1100, 28, 56.2, 60.0);

    app.endUndoGroup();
    alert("Bang Motion: Explainer 60s 'The Extinction of Dinosaurs' built successfully in After Effects!\nComposition: " + compName);
})();
