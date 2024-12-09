<script lang="ts">
	import type * as echarts from 'echarts';
	import type { EChartsOption, EChartOption } from 'echarts';
	import { colorPalette, selectedLineStyle } from '$lib/components/visual/constants';
	import {
		handleClickSelection,
		handleSelectionChange,
		handleHighlightChange
	} from '$lib/components/visual/helperFunctions';
	import EchartsComponent from '$lib/components/visual/EchartsComponent.svelte';

	/** The values to use for the chart. */
	export let values: number[];

	/** The names to use for the indicators (axis). */
	export let indicatorNames: string[] = [];

	export let selectedObjectiveName: string = '';
	/** The indices of the selected items in the chart. */
	export let selectedIndices: number[] = [];

	/** The index of the highlighted item in the chart. */
	export let highlightedIndex: number | undefined = undefined;

	/** The maximum number of items that can be selected in the chart. */
	export let maxSelections: number | undefined = undefined;

	/** If true, the animation of the chart will be disabled. */
	export let disableAnimation: boolean | undefined = undefined;

	/** The aspect ratio of the div container, which contains the chart. */
	export let aspect: string | undefined = 'aspect-[5/3]';

	let chart: echarts.EChartsType;
	let option: EChartOption;

	$: {
		// Create the indicator objects for the radar chart.
		let indObjects: { name: string }[] = [];
		indicatorNames.forEach((name) => {
			indObjects.push({ name: name });
		});

		// Create the option object for the whole chart.
		option = {
			tooltip: {
				trigger: 'axis',
				axisPointer: {
					type: 'shadow'
				},
				formatter: function (params: any) {
					var value = params[0].data; // Assuming you want to check the first value in the axis
					var impactText = value >= 0 ? 'improve' : 'impair'; // Adjust text based on positive or negative value
					if (value == 1) {
						return 'This is the selected objective';
					} else {
						return `Gaining one unit in ${indicatorNames[selectedIndices[0]]} will ${impactText} ${params[0].name} in about ${Math.abs(value.toFixed(5))} units`;
					}
				}
			},
			xAxis: {
				type: 'value',
				position: 'top',
				splitLine: {
					lineStyle: {
						type: 'dashed'
					}
				}
			},
			yAxis: {
				type: 'category',
				inverse: true,
				axisLine: { show: false },
				axisLabel: { show: true },
				axisTick: { show: false },
				splitLine: { show: false },
				data: indicatorNames
			},
			series: [
				{
					type: 'bar',
					data: values,
					label: {
						show: true,
						position: 'inside',
						formatter: function (params: any) {
							return params.value.toFixed(5);
						}
					}
				}
			]
		};

		if (chart) {
			chart.setOption(option);
		}
	}

	let events = {
		click: function (params: {
			dataIndex: number;
			componentType: string;
			seriesIndex: number;
			data: { value: number[] };
		}) {
			console.log(selectedIndices[0]);
		}
	};
</script>

<EchartsComponent {option} bind:chart bind:events {disableAnimation} {aspect} />
