import BABYLON from 'babylonjs';


function degrees_to_radians(degrees) {
    var pi = Math.PI;
    return degrees * (pi / 180);
}


export const createScene = async function (canvas, onDepthRender, onMeshSelected) {
    const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true }); // Generate the BABYLON 3D engine
    engine._caps.textureFloatRender = true;
    // Creates a basic Babylon Scene object
    const scene = new BABYLON.Scene(engine);
    // Creates and positions a free camera
    const camera = new BABYLON.FreeCamera("camera1",
        new BABYLON.Vector3(0, 5, -10), scene);
    camera.fov = degrees_to_radians(30);
    // camera.minZ = 1;
    camera.maxZ = 50.0;
    camera.position.y += -1;
    camera.position.z += -3;
    // Targets the camera to scene origin
    camera.setTarget(BABYLON.Vector3.Zero());
    // This attaches the camera to the canvas
    camera.attachControl(canvas, true);
    // Creates a light, aiming 0,1,0 - to the sky
    const light = new BABYLON.HemisphericLight("light",
        new BABYLON.Vector3(0, 1, 0), scene);
    // Dim the light a small amount - 0 to 1
    light.intensity = 0.7;

    // Built-in 'ground' shape.
    const ground = BABYLON.MeshBuilder.CreateGround("ground",
        { width: 500, height: 500 }, scene);

    const box1 = addBox(scene);

    const backgroundBox = addBox(scene);
    backgroundBox.position.z += 100;
    backgroundBox.scaling.x = 500;
    backgroundBox.scaling.y = 500;

    const nearBackgroundBox = addBox(scene);
    nearBackgroundBox.position.z += 30;
    nearBackgroundBox.scaling.x = 500;
    nearBackgroundBox.scaling.y = 500;

    // RENDER DEPTH
    var depth_renderer = scene.enableDepthRenderer(camera, false);
    //scene.disableDepthRenderer();
    var display_depth = false;

    BABYLON.Effect.ShadersStore['depthbufferPixelShader'] =
        "#ifdef GL_ES\nprecision highp float;\n#endif\n\nvarying vec2 vUV;\nuniform sampler2D textureSampler;\n\nvoid main(void)\n{\nvec4 depth = texture2D(textureSampler, vUV);\ngl_FragColor = vec4(1.0 - depth.r, 1.0 - depth.r, 1.0 - depth.r, 1.0);\n}";

    //alert(test + '\n\n' + BABYLON.Effect.ShadersStore['depthbufferPixelShader']);

    var post_process = new BABYLON.PostProcess('depth_display', 'depthbuffer', null, null, 1.0, null, null, engine, true);
    //post_process.activate(camera, depth_renderer.getDepthMap());
    post_process.onApply = function (effect) {
        effect._bindTexture("textureSampler", depth_renderer.getDepthMap().getInternalTexture());
    }

    // Events

    canvas.addEventListener("render", function (evt) {
        BABYLON.Tools.CreateScreenshot(engine, camera, { precision: 1 }, onDepthRender);
    });

    canvas.addEventListener("rendermodetoggle", function (evt) {
        display_depth = !display_depth;
        if (display_depth) {
            camera.attachPostProcess(post_process);
        } else {
            camera.detachPostProcess(post_process);
        }
    });

    scene.onPointerDown = function () {
        var ray = scene.createPickingRay(scene.pointerX, scene.pointerY, BABYLON.Matrix.Identity(), camera);
        var hit = scene.pickWithRay(ray);
        if (hit.pickedMesh) {
            // console.log("Selected mesh", hit.pickedMesh);
            // currentMesh = hit.pickedMesh;
            onMeshSelected?.(hit.pickedMesh);
        }
    }

    // Create an instance of the DeviceSourceManager and modify the cameraRotation with each rendered frame
    const cameraSpeed = 0.1;
    const dsm = new BABYLON.DeviceSourceManager(scene.getEngine());
    dsm.onDeviceConnectedObservable.add((eventData) => {
        if (eventData.deviceType === BABYLON.DeviceType.Keyboard) {
            const keyboard = dsm.getDeviceSource(BABYLON.DeviceType.Keyboard);

            scene.beforeRender = () => {
                const w = keyboard.getInput(87);
                const a = keyboard.getInput(65);
                const s = keyboard.getInput(83);
                const d = keyboard.getInput(68);


                var forward = camera.getTarget().subtract(camera.position).normalize();
                var right = BABYLON.Vector3.Cross(forward, camera.upVector).normalize();


                if (w === 1) {
                    camera.position.x += cameraSpeed * forward.x;
                    camera.position.y += cameraSpeed * forward.y;
                    camera.position.z += cameraSpeed * forward.z;
                }
                if (s === 1) {
                    camera.position.x -= cameraSpeed * forward.x;
                    camera.position.y -= cameraSpeed * forward.y;
                    camera.position.z -= cameraSpeed * forward.z;
                }
                if (a === 1) {

                    camera.position.x += cameraSpeed * right.x;
                    camera.position.y += cameraSpeed * right.y;
                    camera.position.z += cameraSpeed * right.z;
                }
                if (d === 1) {

                    camera.position.x -= cameraSpeed * right.x;
                    camera.position.y -= cameraSpeed * right.y;
                    camera.position.z -= cameraSpeed * right.z;
                }
            }
        }
    });


    engine.runRenderLoop(function () {
        scene.render();
    });

    window.addEventListener("resize", function () {
        engine.resize();
    });

    return { scene, camera, engine }
};


export function addBox(scene) {
    // random face colors
    const faceColors = [];
    for (let i = 0; i < 6; i++) {
        faceColors.push(new BABYLON.Color3(Math.random(), Math.random(), Math.random()));
    }
    const box = BABYLON.MeshBuilder.CreateBox("box", { size: 1, faceColors: faceColors }, scene);
    return box;
}

export function duplicateObject(mesh) {
    const newMesh = mesh.clone();
    // newMesh.position.x += 1;
    return newMesh;
}