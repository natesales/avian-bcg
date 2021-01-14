<script>
    import {Button, Checkbox, ContentSwitcher, Form, FormGroup, NumberInput, Select, SelectItem, Switch, TextInput} from "carbon-components-svelte";

    let asn;
    let description;
    let peerProfile = 1;
    let validateRpki = true;
    let validateIrr = true;
    let validateMaxPfx = true;
    let asSet;
    let maxPfx4;
    let maxPfx6;
    let router;

    $:{ // TODO: This sends a lot of requests, but on:blur doesnt seem to work
        fetch("__apiRoute__/peeringdb/info", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                "asn": asn
            })
        })
            .then(resp => resp.json())
            .then(data => {
                if (data.meta.success) {
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
</script>

<Form on:submit>
    <FormGroup>
        <NumberInput bind:value={asn} helperText="Autonomous System Number" min={0}/>
        <TextInput bind:value={description} labelText="Session description"/>
    </FormGroup>

    <FormGroup legendText="Peer profile">
        <ContentSwitcher bind:selectedIndex={peerProfile}>
            <Switch text="Upstream"/>
            <Switch text="Peer"/>
            <Switch text="Downstream"/>
        </ContentSwitcher>
    </FormGroup>

    <FormGroup legendText="Validation">
        <Checkbox bind:checked={validateRpki} labelText="RPKI ROV"/>
        <Checkbox bind:checked={validateIrr} labelText="IRR"/>
        <Checkbox bind:checked={validateMaxPfx} labelText="Max prefix"/>
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
        <Select bind:selected={router} id="select-1" labelText="Router">
            <SelectItem text="core1.fmt1" value="core1.fmt1"/>
            <SelectItem text="core1.pdx1" value="core1.pdx1"/>
        </Select>
    </FormGroup>
    <Button type="submit">Submit</Button>
</Form>
