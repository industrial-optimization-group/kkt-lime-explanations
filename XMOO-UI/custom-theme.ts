
import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const myCustomTheme: CustomThemeConfig = {
    name: 'my-custom-theme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-family-heading": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "8px",
		"--theme-rounded-container": "2px",
		"--theme-border-base": "1px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "255 255 255",
		"--on-secondary": "255 255 255",
		"--on-tertiary": "0 0 0",
		"--on-success": "0 0 0",
		"--on-warning": "0 0 0",
		"--on-error": "255 255 255",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #094277 
		"--color-primary-50": "218 227 235", // #dae3eb
		"--color-primary-100": "206 217 228", // #ced9e4
		"--color-primary-200": "194 208 221", // #c2d0dd
		"--color-primary-300": "157 179 201", // #9db3c9
		"--color-primary-400": "83 123 160", // #537ba0
		"--color-primary-500": "9 66 119", // #094277
		"--color-primary-600": "8 59 107", // #083b6b
		"--color-primary-700": "7 50 89", // #073259
		"--color-primary-800": "5 40 71", // #052847
		"--color-primary-900": "4 32 58", // #04203a
		// secondary | #4E46DD 
		"--color-secondary-50": "228 227 250", // #e4e3fa
		"--color-secondary-100": "220 218 248", // #dcdaf8
		"--color-secondary-200": "211 209 247", // #d3d1f7
		"--color-secondary-300": "184 181 241", // #b8b5f1
		"--color-secondary-400": "131 126 231", // #837ee7
		"--color-secondary-500": "78 70 221", // #4E46DD
		"--color-secondary-600": "70 63 199", // #463fc7
		"--color-secondary-700": "59 53 166", // #3b35a6
		"--color-secondary-800": "47 42 133", // #2f2a85
		"--color-secondary-900": "38 34 108", // #26226c
		// tertiary | #4BA2E3 
		"--color-tertiary-50": "228 241 251", // #e4f1fb
		"--color-tertiary-100": "219 236 249", // #dbecf9
		"--color-tertiary-200": "210 232 248", // #d2e8f8
		"--color-tertiary-300": "183 218 244", // #b7daf4
		"--color-tertiary-400": "129 190 235", // #81beeb
		"--color-tertiary-500": "75 162 227", // #4BA2E3
		"--color-tertiary-600": "68 146 204", // #4492cc
		"--color-tertiary-700": "56 122 170", // #387aaa
		"--color-tertiary-800": "45 97 136", // #2d6188
		"--color-tertiary-900": "37 79 111", // #254f6f
		// success | #94CA42 
		"--color-success-50": "239 247 227", // #eff7e3
		"--color-success-100": "234 244 217", // #eaf4d9
		"--color-success-200": "228 242 208", // #e4f2d0
		"--color-success-300": "212 234 179", // #d4eab3
		"--color-success-400": "180 218 123", // #b4da7b
		"--color-success-500": "148 202 66", // #94CA42
		"--color-success-600": "133 182 59", // #85b63b
		"--color-success-700": "111 152 50", // #6f9832
		"--color-success-800": "89 121 40", // #597928
		"--color-success-900": "73 99 32", // #496320
		// warning | #E1B53E 
		"--color-warning-50": "251 244 226", // #fbf4e2
		"--color-warning-100": "249 240 216", // #f9f0d8
		"--color-warning-200": "248 237 207", // #f8edcf
		"--color-warning-300": "243 225 178", // #f3e1b2
		"--color-warning-400": "234 203 120", // #eacb78
		"--color-warning-500": "225 181 62", // #E1B53E
		"--color-warning-600": "203 163 56", // #cba338
		"--color-warning-700": "169 136 47", // #a9882f
		"--color-warning-800": "135 109 37", // #876d25
		"--color-warning-900": "110 89 30", // #6e591e
		// error | #C33175 
		"--color-error-50": "246 224 234", // #f6e0ea
		"--color-error-100": "243 214 227", // #f3d6e3
		"--color-error-200": "240 204 221", // #f0ccdd
		"--color-error-300": "231 173 200", // #e7adc8
		"--color-error-400": "213 111 158", // #d56f9e
		"--color-error-500": "195 49 117", // #C33175
		"--color-error-600": "176 44 105", // #b02c69
		"--color-error-700": "146 37 88", // #922558
		"--color-error-800": "117 29 70", // #751d46
		"--color-error-900": "96 24 57", // #601839
		// surface | #cdd5f4 
		"--color-surface-50": "248 249 253", // #f8f9fd
		"--color-surface-100": "245 247 253", // #f5f7fd
		"--color-surface-200": "243 245 252", // #f3f5fc
		"--color-surface-300": "235 238 251", // #ebeefb
		"--color-surface-400": "220 226 247", // #dce2f7
		"--color-surface-500": "205 213 244", // #cdd5f4
		"--color-surface-600": "185 192 220", // #b9c0dc
		"--color-surface-700": "154 160 183", // #9aa0b7
		"--color-surface-800": "123 128 146", // #7b8092
		"--color-surface-900": "100 104 120", // #646878
		
	}
}