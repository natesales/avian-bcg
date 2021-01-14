<script>
    import {Button, Checkbox, Form, FormGroup, NumberInput, RadioButton, RadioButtonGroup, Select, SelectItem, TextInput} from "carbon-components-svelte";

    function getPeeringDbData(asn) {
        fetch()
    }
</script>

<Form on:submit>
    <FormGroup legendText="Neighbor">
        <NumberInput inline helperText="Autonomous System Number"/>
        <TextInput inline labelText="Session description"/>
    </FormGroup>

    <FormGroup legendText="Validation">
        <Checkbox checked id="rpki-rov" labelText="RPKI ROV"/>
        <Checkbox checked id="irr" labelText="IRR"/>
        <Checkbox checked id="max-prefix" labelText="Max prefix"/>
    </FormGroup>

    <FormGroup legendText="Peer profile">
        <RadioButtonGroup selected="peer">
            <RadioButton id="upstream" labelText="Upstream" value="upstream"/>
            <RadioButton id="peer" labelText="Peer" value="peer"/>
            <RadioButton id="downstream" labelText="Downstream" value="downstream"/>
        </RadioButtonGroup>
    </FormGroup>
    <FormGroup>
        <Select id="select-1" labelText="Router">
            <SelectItem text="core1.fmt1" value="core1.fmt1"/>
            <SelectItem text="core1.pdx1" value="core1.pdx1"/>
        </Select>
    </FormGroup>
    <Button type="submit">Submit</Button>
</Form>
