<script lang="ts">
	import { onMount } from 'svelte';
	import axios from 'axios';
	import { store } from '$lib/store';

	let numObjectives: number;
	let referencePoint: number[];
	let lagrangeMultipliers: number[];
	let partialTradeoffs: number[][];
	let fx: number[];
	let ideal: number[];
	let nadir: number[];

	// Subscribe to the store
	$: {
		$store;
		numObjectives = $store.numObjectives;
		referencePoint = $store.referencePoint;
		lagrangeMultipliers = $store.lagrangeMultipliers;
		partialTradeoffs = $store.partialTradeoffs;
		fx = $store.fx;
		ideal = $store.ideal;
		nadir = $store.nadir;
	}

	// Function to get solution and update the store
	const getDetails = async () => {
		try {
			const response = await axios.post('http://127.0.0.1:5000/get_details_problem');
			store.update((state) => ({
				...state,
				ideal: response.data.ideal,
				nadir: response.data.nadir,
				referencePoint: response.data.ideal // assuming you want to initialize referencePoint with ideal
			}));
		} catch (error) {
			console.error('Error fetching solution:', error);
		}
	};

	// Function to get solution and update the store
	const getSolution = async () => {
		try {
			// Get current reference point from the store
			const response = await axios.post('http://127.0.0.1:5000/get_solution', {
				reference_point: referencePoint
			});

			// Update the store with new data
			store.update((state) => ({
				...state,
				lagrangeMultipliers: response.data.lagrange_multipliers,
				partialTradeoffs: response.data.partial_tradeoffs,
				fx: response.data.fx
			}));
		} catch (error) {
			console.error('Error fetching solution:', error);
		}
	};

	// Function to update reference point in the store
	function updateReferencePoint(index: number, value: number) {
		store.update((state) => {
			const newReferencePoint = [...state.referencePoint];
			newReferencePoint[index] = value;
			return { ...state, referencePoint: newReferencePoint };
		});
	}

	onMount(() => {
		getDetails();
	});
</script>

<div class="container">
	<div>
		<h3>Partial Tradeoffs</h3>
		<div class="table-container">
			<!-- Native Table Element -->
			<table class="table table-hover">
				<thead>
					<tr>
						<th>-</th>
						{#each Array(numObjectives).fill(undefined) as _, index}
							<th>Objective {index + 1}</th>
						{/each}
					</tr>
				</thead>
				<tbody>
					{#each $store.partialTradeoffs as row, i}
						<tr>
							<td>Objective {i + 1}</td>
							{#each row as tradeoff, j}
								<td>{tradeoff}</td>
							{/each}
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
