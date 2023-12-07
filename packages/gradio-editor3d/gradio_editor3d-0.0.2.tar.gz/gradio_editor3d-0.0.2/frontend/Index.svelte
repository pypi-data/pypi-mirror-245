<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";
	import { onMount } from "svelte";
	import { createScene, addBox, duplicateObject } from "./gui";
	import ValueAdjuster from "./ValueAdjuster.svelte";
	import BABYLON from "babylonjs";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
	}>;
	export let label = "Editor3D";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let interactive: boolean;

	let el: HTMLCanvasElement;
	const container = true;

	async function handle_change(): Promise<void> {
		await tick();
		// gradio.dispatch("input");
		gradio.dispatch("change");
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			gradio.dispatch("submit");
		}
	}
	let scene;
	let engine;
	let camera;
	let selectedMesh;

	const onMeshSelected = (mesh) => {
		selectedMesh = mesh;
	};
	// Events
	const onRender = (renderedImage) => {
		value = renderedImage;
		// value && gradio.dispatch("change");
		handle_change();
	};

	const render = () => {
		BABYLON.Tools.CreateScreenshot(
			engine,
			camera,
			{ precision: 1 },
			onRender,
		);
	};

	const toggleRenderMode = () => {
		if (engine) {
			// dispatch 'rendermodetoggle' event
			const event = new CustomEvent("rendermodetoggle");
			el.dispatchEvent(event);
		}
	};

	onMount(async () => {
		({ scene, engine, camera } = await createScene(
			el,
			onRender,
			onMeshSelected,
		));
	});

	const scaledR = (value) => (value ? (value * Math.PI) / 180 : 0);
	const unscaledR = (value) => (value ? (value / Math.PI) * 180 : 0);
	const scaledT = (value) => (value ? value * 0.1 : 0);
	const unscaledT = (value) => (value ? value / 0.1 : 0);
	const scaledS = (value) => (value ? value * 0.1 : 0);
	const unscaledS = (value) => (value ? value / 0.1 : 0);

	// $: if (value === null) value = "";

	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	// $: value, handle_change();
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}

	<!-- <label class:container> -->
	{#if show_label}
		<BlockTitle>{label}</BlockTitle>
	{/if}
	<div class="app-container">
		<div class="canvas-section" id="canvas">
			<canvas bind:this={el}></canvas>
		</div>
		<div class="controls-section">
			<div class="render-controls">
				<!-- Render Buttons -->
				<button on:click={render}>Render</button>
				<button on:click={toggleRenderMode}>Toggle Mode</button>
			</div>
			<div class="mesh-controls">
				<!-- Action Buttons -->
				<button
					on:click={() => {
						selectedMesh = addBox(scene);
					}}>Add Box</button
				>
				<button on:click={() => selectedMesh?.dispose()}>Delete</button>
				<button
					on:click={() => {
						selectedMesh = duplicateObject(selectedMesh);
					}}>Duplicate</button
				>
			</div>

			<div class="transform-controls">
				<div class="control-group rotation">
					<div class="group-title">Rotation</div>
					<ValueAdjuster
						label="Rx"
						value={unscaledR(selectedMesh?.rotation.x)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.rotation.x = scaledR(
									e.detail.value,
								);
							}
						}}
					/>

					<ValueAdjuster
						label="Ry"
						value={unscaledR(selectedMesh?.rotation.y)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.rotation.y = scaledR(
									e.detail.value,
								);
							}
						}}
					/>
					<ValueAdjuster
						label="Rz"
						value={unscaledR(selectedMesh?.rotation.z)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.rotation.z = scaledR(
									e.detail.value,
								);
							}
						}}
					/>
				</div>

				<div class="control-group translation">
					<div class="group-title">Translation</div>

					<ValueAdjuster
						label="Tx"
						scalingFactor={1}
						value={unscaledT(selectedMesh?.position.x)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.position.x = scaledT(
									e.detail.value,
								);
							}
						}}
					/>

					<ValueAdjuster
						label="Ty"
						scalingFactor={1}
						value={unscaledT(selectedMesh?.position.y)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.position.y = scaledT(
									e.detail.value,
								);
							}
						}}
					/>

					<ValueAdjuster
						label="Tz"
						scalingFactor={1}
						value={unscaledT(selectedMesh?.position.z)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.position.z = scaledT(
									e.detail.value,
								);
							}
						}}
					/>
				</div>
				<div class="control-group scale">
					<div class="group-title">Scale</div>
					<ValueAdjuster
						label="Sx"
						value={unscaledS(selectedMesh?.scaling.x)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.scaling.x = scaledS(
									e.detail.value,
								);
							}
						}}
					/>

					<ValueAdjuster
						label="Sy"
						value={unscaledS(selectedMesh?.scaling.y)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.scaling.y = scaledS(
									e.detail.value,
								);
							}
						}}
					/>

					<ValueAdjuster
						label="Sz"
						value={unscaledS(selectedMesh?.scaling.z)}
						on:change={(e) => {
							if (selectedMesh) {
								selectedMesh.scaling.z = scaledS(
									e.detail.value,
								);
							}
						}}
					/>
				</div>
				<div class="control-group camera">
					<div class="group-title">Camera</div>
					<!-- Camera Transforms -->
					<ValueAdjuster
						label="FoV"
						value={unscaledR(camera?.fov)}
						on:change={(e) => {
							if (camera) {
								camera.fov = scaledR(e.detail.value);
							}
						}}
					/>
					<ValueAdjuster
						label="Z"
						value={unscaledT(camera?.maxZ)}
						on:change={(e) => {
							if (camera) {
								camera.maxZ = scaledT(e.detail.value);
							}
						}}
					/>
				</div>
			</div>
		</div>
	</div>
	<!-- </label> -->
</Block>

<style>
	.app-container {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 1rem;
		padding: 1rem;
		align-items: center; /* Aligns the top of the canvas with the top of the controls */
		/* height: 70vh; */
	}

	.canvas-section {
		display: flex;
		justify-content: center;
		align-items: start; /* Aligns the canvas to the top */
	}

	canvas {
		border: 1px solid #ccc; /* Adds a border for visibility */
		box-sizing: border-box; /* Includes border in the width and height calculations */
		/* max-width: 80vh; */
		/* max-height: 80vh; */
		/* width: 80vh; */
		/* height: 80vh; */
		width: 500px;
		height: 500px;
		max-width: 100%; /* Ensures the canvas is not wider than its container */
		aspect-ratio: 1 / 1; /* Maintains a square aspect ratio */
		z-index: 4;
		pointer-events: all;
		cursor: pointer;
	}

	/* Media query for devices with width larger than height */
	@media (min-aspect-ratio: 1/1) {
		canvas {
			/* width: 80vh; */
			/* height: 80vh; */
			width: 500px;
			height: 500px;
		}
	}

	/* Media query for smaller devices */
	@media (max-width: 768px) {
		.app-container {
			grid-template-columns: 1fr; /* Stacks canvas and controls on top of each other */
			gap: 0.5rem;
		}

		.canvas-section,
		.controls-section {
			width: 100%; /* Takes up all available space */
		}

		canvas {
			/* max-width: 80vh; */
			/* max-height: 80vh; */
			width: 80vw;
			height: 80vw;
		}
	}

	.controls-section {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.mesh-controls {
		display: flex;
		gap: 0.5rem;
		justify-content: center;
		margin-bottom: 2rem; /* Adds space below the mesh control buttons */
	}

	.render-controls {
		display: flex;
		gap: 0.5rem;
		justify-content: center;
	}

	button {
		background-color: #4caf50;
		color: white;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	button:hover {
		background-color: #45a049;
	}

	.render-controls button {
		background-color: #008cba;
	}

	.render-controls button:hover {
		background-color: #007b9e;
	}

	.control-group {
		background-color: #f8f8f8;
		padding: 0.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.group-title {
		font-weight: bold;
		color: #444;
		margin-bottom: 0.5rem;
	}
</style>
