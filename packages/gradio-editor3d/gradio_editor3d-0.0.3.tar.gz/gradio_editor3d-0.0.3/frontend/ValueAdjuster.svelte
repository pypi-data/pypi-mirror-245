<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    export let label = "";
    export let value = 0;
    export let scalingFactor = 2;

    let editable = false; // State for toggling edit mode

    function emitChange() {
        dispatch("change", { value: value });
    }

    function toggleEdit() {
        editable = !editable;
        if (!editable) {
            // Emit change when exiting edit mode
            emitChange();
        }
    }

    let startX;
    function handleMouseDown(event) {
        startX = event.clientX;
        event.target.addEventListener("mousemove", handleMouseMove);
        event.target.addEventListener("mouseup", handleMouseUp);
        event.target.setPointerCapture(event.pointerId);
    }

    function handleMouseMove(event) {
        const screenWidth = window.innerWidth;
        const dx = (event.clientX - startX) / screenWidth;
        value += Math.sign(dx) * scalingFactor;
        startX = event.clientX;
        emitChange();
    }

    function handleMouseUp(event) {
        event.target.removeEventListener("mousemove", handleMouseMove);
        event.target.removeEventListener("mouseup", handleMouseUp);
    }

    function handleDoubleClick() {
        toggleEdit();
    }

    function increment() {
        value += 1;
        emitChange();
    }

    function decrement() {
        value -= 1;
        emitChange();
    }
</script>

<div class="container">
    <span class="label">{label}</span>
    <button on:click={decrement}>-</button>
    {#if editable}
        <input
            class="value"
            type="number"
            bind:value
            on:blur={toggleEdit}
            on:keydown={(e) => {
                if (e.key === "Enter") toggleEdit();
            }}
        />
    {:else}
        <div
            class="value"
            on:pointerdown={handleMouseDown}
            on:dblclick={handleDoubleClick}
            on:click|stopPropagation
        >
            {value.toPrecision(2)}
        </div>
    {/if}
    <button on:click={increment}>+</button>
</div>

<style>
    .container {
        display: flex;
        align-items: center;
        justify-content: center;
        user-select: none;
        background-color: #1e1e1e; /* Dark background */
        padding: 2px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(255, 255, 255, 0.2);
    }
    .label,
    .value {
        color: #fff; /* White text for visibility */
    }
    .value {
        background-color: #333; /* Darker background for the value display */
        border: 1px solid #555; /* Border for the value display */
        cursor: ew-resize;
        display: inline-block;
        margin: 0 1rem; /* Space around the value */
        padding: 1px 5px; /* Padding for the value display */
        border-radius: 4px; /* Rounded corners for the value display */
        font-size: 1rem; /* Adequate font size for readability */
        text-align: center;
        width: 70px;
    }
    button {
        cursor: pointer;
        background-color: #007bff; /* Blue background */
        color: white; /* White text */
        border: none; /* No border */
        padding: 0px 5px; /* Padding inside the button */
        margin: 0 5px; /* Spacing around buttons */
        border-radius: 4px; /* Rounded corners for buttons */
        transition: background-color 0.3s; /* Smooth background transition for buttons */
    }
    button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
</style>
