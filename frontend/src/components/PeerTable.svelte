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
    <DataTable headers={[
        { key: "description", value: "Description" },
        { key: "asn", value: "ASN" },
        { key: "neighborAddress", value: "Address" },
        { key: "router", value: "Router" },
        { key: "profile", value: "Profile" },
        { key: "asSet", value: "AS-Set" },
        { key: "maxPfx4", value: "IPv4 Prefixes" },
        { key: "maxPfx6", value: "IPv6 Prefixes" },
        { key: "validateRpki", value: "RPKI Validation" },
        { key: "validateIrr", value: "IRR Validation" },
        { key: "validateMaxPfx", value: "Max-Prefix Validation" },
    ]} rows={peers}/>
</main>
