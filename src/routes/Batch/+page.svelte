<script>
	// @ts-nocheck
	import { exclude_internal_props } from 'svelte/internal';
	import duplicates from '../../data/duplicates.json';

	export let out = { displayname: '' };
	export let out2 = [];
	export const exclusions = [];
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
		const a = error.replace('#code', '<span class="code">').replace('/code', '</span>');
		document.getElementById('alert').classList.remove('hidden');
		document.getElementById('alertbox').classList.remove('hidden');
		document.getElementById(
			'spancontainer'
		).innerHTML = `<span>${a}</span><div style="padding: 1rem;"></div>`;
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
		let re;

		if (displayRename(result.displayname) in duplicates.data) {
			// if the item is excluded from standard CIT
			re = `type=item\nitems=${result.itemid}\nnbt.ExtraAttributes.id=${
				document.getElementById('iname').value
			}`;
		} else {
			// if the item is included in standard CIT
			re = `type=item\nitems=${result.itemid}\nnbt.display.Name=ipattern:*${displayRename(
				result.displayname
			)}*`;
		}
		re += `\ntexture=${internalName}`;

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

<label for="file">Upload your file(s)</label>

<!-- File select button -->
<input type="file" id="file" name="fileToUpload" multiple />
<!-- Submit form -->
<form autocomplete="off" class="main">
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

				for (let i = 0; i < internalFiles.length; i++) { // Iter through each file
					const file = internalFiles[i]; // get file name (should look like ITEM_ID.png)

					let internalName = file.name.split('.')[0].toUpperCase(); // get internal name (file name without extension and capitalized)
						try { // Pull data from NotEnoughUpdates repo (https://github.com/NotEnoughUpdates/NotEnoughUpdates-REPO)
							getJSON(
								`https://raw.githubusercontent.com/NotEnoughUpdates/NotEnoughUpdates-REPO/master/items/${internalName}.json`
							).then((result) => {
								if (!processData(result, internalName)) {
                                    failed.push(internalName);
                                } // Pass internal name and JSON data to processData()
							});
						} catch (error) { // Failed to find json file -> Either it doesn't exist or the request was closed (further processing necessary)
							errorWindow(`Error: ${error}`); // Show error window
						}
				}
                errorWindow(`Failed to find the following files: #code${failed.join(', ')}/code`);
			}}
		/>
	</div>
	<div class="linebreak" />
	<div class="linebreak" />
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
<div id="alert" class="hidden" on:click={() => hideErrorWindow()}>
	<div id="alertbox" class="hidden">
		<div id="spancontainer" />
		<input
			class="enter"
			id="ok"
			type="button"
			name="ok"
			value="OK"
			on:click={() => {
				console.log('hello!');
			}}
		/>
	</div>
</div>
