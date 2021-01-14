<script>
    import {DataTable} from "carbon-components-svelte";

    let peers;

    function updateTable() {
        fetch("__apiRoute__/sessions", {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        })
            .then(resp => resp.json())
            .then(data => {
                if (data.meta.success) {
                    peers = data.data;
                } else {
                    alert(data.meta.message)
                }
            })
    }

    updateTable();

    // Update table every 2 seconds
    setInterval(updateTable, 2000)
</script>

<main>
    <h3>Session Overview</h3>
    <br>
    <DataTable headers={[{ key: "description", value: "Description" }, { key: "asn", value: "ASN" }]} rows={peers}/>
</main>
