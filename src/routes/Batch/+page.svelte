<script>
	// @ts-nocheck
	import { exclude_internal_props } from 'svelte/internal';
	import duplicates from '../../data/duplicates.json';
	import items from '../../data/items.json';

	const preferredMethod = 0;
	/*
	0 = ID
	1 = ipattern
	*/

	let out = {};
	let out2 = [];
	const exclusions = [];
	export const inputs = [
		{
			name: 'iname',
			title: 'Internal Name',
			placeholder: 'END_SWORD'
		},
		{
			name: 'txname',
			title: 'Texture Name',
			placeholder: 'texture.png',
			split: true // broken atm
		},
		{
			name: 'fname',
			title: 'File Name',
			placeholder: 'texture.properties'
		},
		{
			name: 'jname',
			title: 'Model Name',
			placeholder: 'model.json'
		}
	];

	// Unused for now (I forgot what I made it for so i'll leave it here)
	async function getFiles() {
		const data = await request.formData();
		const files = data.getAll('file');
		return files;
	}

	// Download file from browser
	function download(data, filename, type) {
		let file = new Blob([data], { type: type });
		if (window.navigator.msSaveOrOpenBlob) window.navigator.msSaveOrOpenBlob(file, filename);
		else {
			// Others
			let a = document.createElement('a'),
				url = URL.createObjectURL(file);
			a.href = url;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			setTimeout(function () {
				document.body.removeChild(a);
				window.URL.revokeObjectURL(url);
			}, 0);
		}
	}

	// Remove minecraft formatting from string
	function displayRename(input) {
		let output = '';
		('§a' + input).split('§').forEach((part) => {
			output += part.substring(1);
		});
		return output;
	}

	// Get JSON from a URL
	async function getJSON(input) {
		const response = await fetch(input, {
			method: 'GET'
		});

		if (response.ok) {
			return response.json();
		} else {
			return false;
		}
	}

	// Open an error window on screen
	function errorWindow(error) {
		const htmlPart = error.replace('#code', '<span class="code">').replace('/code', '</span>');
		document.getElementById('alert').classList.remove('hidden');
		document.getElementById('alertbox').classList.remove('hidden');
		document.getElementById(
			'spancontainer'
		).innerHTML = `<span>${htmlPart}</span><div style="padding: 1rem;"></div>`;
	}

	// Hide error window on screen
	function hideErrorWindow() {
		document.getElementById('alert').classList.add('hidden');
		document.getElementById('alertbox').classList.add('hidden');
		document.getElementById('spancontainer').innerHTML = '';
	}

	// Process data from NEU repository, using JSON and internal name
	// TODO : CHECK IF RESULT IS JSON OR TEXT
	function processData(result, internalName) {
		let re = `\nitems=${result.itemid}\ntexture=${internalName}.png\n`;
		if (preferredMethod === 0) {
			re += `nbt.ExtraAttributes.id=${internalName}`;
		} else if (preferredMethod === 1) {
			if (displayRename(result.displayname) in duplicates.data) {
				// if the item is excluded from standard CIT
				re = `nbt.ExtraAttributes.id=${internalName}`;
			} else {
				// if the item is included in standard CIT
				re = `nbt.display.Name=ipattern:*${displayRename(result.displayname)}*`;
			}
		}

		out2.push({
			// output for file editor / download
			content: re,
			fname: internalName
		});

		// unhide download button
		document.getElementById('downloadcontainer').classList.remove('hidden');
		document.getElementById('downloadbutton').classList.remove('hidden');
	}
</script>

<title>CIT Generator - Items</title>

<h1 class="box-inner">
	<a class="linkto" href="/">Item CIT Generator</a>
</h1>
<div class="linebreak" />

<!-- File select button -->

<!-- Submit form -->
<form autocomplete="off" class="main">
	<div class="labelgroup submit inputs">
		<input type="file" id="file" name="fileToUpload" multiple />
		<input id="fakefile" class="" value="Select Files" />
	</div>
	<div class="labelgroup submit">
		<!-- Submit button -->
		<input
			class="submit"
			type="button"
			name="submit"
			value="Submit"
			on:click={function () {
				let internalFiles = document.getElementById('file').files; // Take files from #file
				let failed = [];

				for (let i = 0; i < internalFiles.length; i++) {
					// Iter through each file
					const file = internalFiles[i]; // get file name (should look like ITEM_ID.png)

					let internalName = file.name.split('.')[0].toUpperCase(); // get internal name (file name without extension and capitalized)
					try {
						processData(items[internalName], internalName);
					} catch (error) {
						failed.push(internalName);
						console.error(error); // Failed to find json file -> it doesn't exist
						errorWindow(`Error: #code${error}/code<br>Texture: ${internalName}`); // Show error window
					}
				}
			}}
		/>
	</div>
	<div class="labelgroup submit hidden" id="downloadcontainer">
		<input
			class="submit hidden"
			id="downloadbutton"
			type="button"
			name="download"
			value="Download"
			on:click={() => {
				out2.forEach((file) => {
					download(file.content, `${file.fname}.properties`, 'text'); // Download every file that has been properly created
				});
				window.location.reload(); // Reload window (I don't know why this is here either, but I'm leaving it)
			}}
		/>
	</div>
</form>
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	id="alert"
	class="hidden"
	on:click={() => hideErrorWindow()}
	on:keydown={(e) => {
		if (e.key === 'Enter') {
			hideErrorWindow();
		}
	}}
>
	<div id="alertbox" class="hidden">
		<div id="spancontainer" />
		<input class="enter" id="ok" type="button" name="ok" value="OK" />
	</div>
</div>
