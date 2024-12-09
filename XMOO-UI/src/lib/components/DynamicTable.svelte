<script lang="ts">
	export let title = 'Table';
	export let tableHeader: string[];
	export let tableData: number[][];
	export let decimalPlaces: number;
</script>

<div class="container">
	<h2>{title}</h2>
	<div class="table-container">
		<!-- Native Table Element -->
		<table class="table table-hover">
			<thead>
				<tr>
					{#each tableHeader as columnHeading}
						<th>{columnHeading}</th>
					{/each}
				</tr><tr />
			</thead>
			<tbody>
				{#each tableData as row}
					<tr>
						{#each row as cell}
							<td>{cell.toFixed(decimalPlaces)}</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
