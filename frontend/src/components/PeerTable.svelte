<script>
    import {DataTable} from "carbon-components-svelte";

    const rows=[
        { id: "a", name: "Load Balancer 3", protocol: "HTTP", port: 3000, rule: "Round robin" },
        { id: "b", name: "Load Balancer 1", protocol: "HTTP", port: 443, rule: "Round robin" },
        { id: "c", name: "Load Balancer 2", protocol: "HTTP", port: 80, rule: "DNS delegation" },
        { id: "d", name: "Load Balancer 6", protocol: "HTTP", port: 3000, rule: "Round robin" },
        { id: "e", name: "Load Balancer 4", protocol: "HTTP", port: 443, rule: "Round robin" },
        { id: "f", name: "Load Balancer 5", protocol: "HTTP", port: 80, rule: "DNS delegation" }
    ]
</script>

<main>
    <h3>Session Overview</h3>
    <br>
    <DataTable headers={[{ key: "name", value: "Name" }, { key: "asn", value: "ASN" }, { key: "neighbor-address", value: "Neighbor Address" }, { key: "local-address", value: "Local Address" }]} rows={rows}/>
</main>