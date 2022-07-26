# chain-function
An Azure function that generates a word from a Markov chain.

Usage in JavaScript:

```
let response = fetch("https://pamelaschainfunction-apim.azure-api.net/PamelasChainFunction/ChainFunction?kind=planet", {
headers: {
    "Ocp-Apim-Subscription-Key": "<KEY HERE>",
  }
}).then((response) => response.text())
.then(console.log)
.catch(console.error);
```