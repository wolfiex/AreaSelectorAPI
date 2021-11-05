<script>
	import Select from "svelte-select";

	export const limit = 5;
	export let selection = null;
	let select;

	function loadOptions(filterText) {
		// filterText = filterText ? filterText.replace(" ", "_") : "";
		const postcode = filterText.match(/\d/);
		const check = postcode? 'postcode':'name'

		var a =  new Promise((resolve, reject) => {
			const xhr = new XMLHttpRequest();
			xhr.open(
				"GET",
				`http://127.0.0.1:5002/${check}/${filterText}/${limit}`
			);
			xhr.send();

			xhr.onload = () => {
				if (xhr.status >= 200 && xhr.status < 300) {
					setTimeout(
						resolve(
							JSON.parse(xhr.response)
						),
						2000
					);
				} else {
					reject();
				}
			};
		});  
	return a
	}


function handleSelect(event) {
    console.warn(event.detail)

	// if ( event.detail[0].match(/\d/) ){
	// 	var id = event.detail()
	// }
	// no need as we are only using lad 
	// postcodes have lsoa too


		fetch(`http://127.0.0.1:5002/lad/${event.detail[1]}`)
			.then(e=>e.json())
			.then(response => {
				// console.warn(response)
				selection = response[0]
			})
			.catch(error => {
				// handle the error
			});



  }





	const optionIdentifier = 0;
	const getOptionLabel = (option) => option[0]  + ((!option[2] ^ option[0].match(/\d/))
	?'':' (region)') ;
	const getSelectionLabel = (option) => option[0];



$:selection,console.warn(selection)


</script>

<h2>Location Selector</h2>
<Select
	{loadOptions}
	{optionIdentifier}
	{getSelectionLabel}
	{getOptionLabel}
	on:select={handleSelect}
	noOptionsMessage='Please enter a valid area description.'
	bind:this={select}
	placeholder="Area or Postcode"
/>

<style>
</style>
