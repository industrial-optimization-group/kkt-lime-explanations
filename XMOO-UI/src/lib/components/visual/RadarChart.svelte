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
	export let values: number[][];

	/** The names to use for the indicators (axis). */
	export let indicatorNames: string[] = [];

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
	let maxValues = [6.34, 3.44487, 7.5, 0];
	let minValues = [4.751, 2.85346, 0.32111, -9.70667];
	$: if (selectedIndices && chart) {
		handleSelectionChange(chart, selectedIndices, maxSelections);
	}

	$: if (chart) {
		handleHighlightChange(chart, highlightedIndex);
	}

	$: {
		// Create the indicator objects for the radar chart.
		let indObjects: { name: string; max: number; min: number }[] = [];
		indicatorNames.forEach((name, i) => {
			indObjects.push({ name: name, max: maxValues[i], min: minValues[i] });
		});

		// Create the series data for the radar chart.

		let seriesData: { value: number[]; name: string; symbol: string }[] = [];
		for (let i = 0; i < values.length; i++) {
			if (i == 0) {
				seriesData.push({
					value: values[i].map((num) => parseFloat(num.toFixed(5))),
					name: 'Obtained solution',
					symbol: 'circle'
				});
			} else {
				if (values[i].length > 0) {
					seriesData.push({
						value: values[i].map((num) => parseFloat(num.toFixed(5))),
						name: 'Approximated solution',
						symbol: 'rect'
					});
				}
			}
		}

		// Create the option object for the whole chart.
		option = {
			tooltip: {},
			color: ['#1f7095', '#07d2c9', '#56A3F1', '#FF917C'],
			legend: { orient: 'vertical', left: 'left', top: 'top' },
			radar: {
				shape: 'circle',
				indicator: indObjects,
				scale: true,
				//splitNumber: 1, // Force only one split to reduce the number of labels

				axisLabel: {
					show: false,
					showMinLabel: false,
					showMaxLabel: true,
					hideOverlap: true
				}
			},
			series: [
				{
					symbol: 'none',
					type: 'radar',
					selectedMode: 'multiple',
					// TODO: Select has type error:Object literal may only specify known properties, and 'select' does not exist in type 'SeriesLine | SeriesPie | SeriesScatter | SeriesEffectScatter | SeriesRadar | SeriesTree | ... 14 more ... | SeriesCustom
					//  eslint-disable-next-line @typescript-eslint/ban-ts-comment
					// @ts-ignore -- Error says that disabled doesn't exist in the echarts series type, but in the documentation it exists. Might be because it's a new property, so they have not updated the type yet. https://echarts.apache.org/en/option.html#series-bar.emphasis.disabled
					select: {
						lineStyle: selectedLineStyle
					},
					data: seriesData
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
			selectedIndices = handleClickSelection(chart, params, selectedIndices, maxSelections);
		},
		mouseover: function (params: { dataIndex: number }) {
			highlightedIndex = params.dataIndex;
		},
		mouseout: function () {
			highlightedIndex = undefined;
		}
	};
</script>

<EchartsComponent {option} bind:chart bind:events {disableAnimation} {aspect} />
