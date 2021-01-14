<script>
    import {Form, FormGroup, Loading, Select, SelectItem, CodeSnippet} from "carbon-components-svelte";
    import {config} from "../stores";

    let loading = true;
    let routerConfig;
    let router = Object.keys($config["routers"])[0];

    function showRouterConfig() {
        fetch("__apiRoute__/render/" + router, {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        })
            .then(resp => resp.json())
            .then(data => {
                console.log(data.meta)
                if (data.meta.success) {
                    routerConfig = data.data;
                } else {
                    routerConfig = "// Undefined"
                    alert(data.meta.message)
                }
                loading = false;
            })
    }

    showRouterConfig()
</script>

<main>
    <Form on:submit={() => {}}>
        <h4>Router config for <code>{router}</code></h4>
        <br>
        <FormGroup>
            <Select bind:selected={router} labelText="Router" on:change={showRouterConfig}>
                {#each Object.keys($config.routers) as router}
                    <SelectItem text={router} value={router}/>
                {/each}
            </Select>
        </FormGroup>
    </Form>

    {#if loading}
        <Loading/>
    {:else}
        <CodeSnippet hideCopyButton expanded type="multi" code={routerConfig}/>
    {/if}
</main>
