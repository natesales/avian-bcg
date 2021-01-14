<script>
    import {Button, Checkbox, ContentSwitcher, Form, FormGroup, InlineLoading, NumberInput, Select, SelectItem, Switch, TextInput} from "carbon-components-svelte";
    import {config} from "../stores";

    let asn;
    let description;
    let profile = 1;
    let validateRpki = true;
    let validateIrr = true;
    let validateMaxPfx = true;
    let asSet;
    let maxPfx4;
    let maxPfx6;
    let router = Object.keys($config["routers"])[0];
    let neighborAddress;

    let isLoading = false;

    function addSession() {
        isLoading = true;

        switch(profile) {
            case 0:
                profile = "upstream"
                break;
            case 1:
                profile = "peer"
                break;
            default:
                profile = "downstream"
        }

        fetch("__apiRoute__/sessions", {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                asn,
                description,
                profile,
                validateRpki,
                validateIrr,
                validateMaxPfx,
                asSet,
                maxPfx4,
                maxPfx6,
                router,
                neighborAddress
            })
        })
            .then(resp => resp.json())
            .then(data => {
                if (data.meta.success) {
                    console.log(data)
                } else {
                    alert(data.meta.message)
                }
                isLoading = false;
                neighborAddress = "";
                alert(data.meta.message)
            })
    }

    $: {
        if (asn !== undefined && asn > 0) {
            fetch("https://peeringdb.com/api/net?asn=" + asn, {
                method: "GET"
            })
                .then(resp => resp.json())
                .then(data => {
                    if (data && data.data[0]) {
                        if (data.data[0].name) {
                            description = data.data[0].name;
                        }
                        if (data.data[0].irr_as_set) {
                            asSet = data.data[0].irr_as_set;
                        }
                        if (data.data[0].info_prefixes4) {
                            maxPfx4 = data.data[0].info_prefixes4;
                        }
                        if (data.data[0].info_prefixes6) {
                            maxPfx6 = data.data[0].info_prefixes6;
                        }
                    }
                })
        }
    }
</script>

<main>
    <Form on:submit={() => addSession()}>
        <h4>Add a new neighbor adjacency</h4>
        <br>
        <FormGroup>
            <NumberInput bind:value={asn} helperText="Autonomous System Number" min={0}/>
            <TextInput bind:value={description} labelText="Session description"/>
        </FormGroup>

        <FormGroup legendText="Peer profile">
            <ContentSwitcher bind:selectedIndex={profile}>
                <Switch text="Upstream"/>
                <Switch text="Peer"/>
                <Switch text="Downstream"/>
            </ContentSwitcher>
        </FormGroup>

        <FormGroup legendText="Filtering">
            <Checkbox bind:checked={validateRpki} labelText="RPKI ROV"/>
            <Checkbox bind:checked={validateIrr} labelText="IRR"/>
            <Checkbox bind:checked={validateMaxPfx} labelText="Max prefix"/>
            <Checkbox disabled labelText="Peerlock"/>
        </FormGroup>

        {#if validateIrr}
            <FormGroup>
                <TextInput labelText="AS-SET" bind:value={asSet}/>
            </FormGroup>
        {/if}

        {#if validateMaxPfx}
            <FormGroup>
                <NumberInput label="IPv4 Prefix Limit" bind:value={maxPfx4}/>
                <NumberInput label="IPv6 Prefix Limit" bind:value={maxPfx6}/>
            </FormGroup>
        {/if}

        <FormGroup>
            <Select bind:selected={router} labelText="Router">
                {#each Object.keys($config.routers) as router}
                    <SelectItem text={router} value={router}/>
                {/each}
            </Select>
        </FormGroup>

        <FormGroup>
            <TextInput bind:value={neighborAddress} labelText="Neighbor Address"/>
        </FormGroup>

        <Button type="submit">
            {#if isLoading}
                <InlineLoading/>
            {:else}
                Submit
            {/if}
        </Button>
    </Form>
</main>