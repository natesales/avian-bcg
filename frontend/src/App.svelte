<script>
    import {Breadcrumb, BreadcrumbItem, Column, Content, Grid, Row, Select, SelectItem, Tab, TabContent, Tabs} from "carbon-components-svelte";
    import Header from "./components/Header.svelte";
    import Theme from "./components/Theme.svelte";
    import Footer from "./components/Footer.svelte";
    import PeerForm from "./components/PeerForm.svelte";
    import PeerTable from "./components/PeerTable.svelte";
    import {onMount} from "svelte";
    import {config} from "./stores";

    let theme = "g10";

    let ready = false;

    onMount(() => {
        fetch("__apiRoute__/config", {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        })
            .then(resp => resp.json())
            .then(data => {
                    if (data.meta.success) {
                        config.set(data.data);
                        ready = true;
                    }
                })
    })
</script>

<Theme bind:theme persist>
    <Header/>
    <Content style="background: none; padding: 1rem">
        {#if ready}
        <Grid>
            <Row>
                <Column lg="{16}">
                    <Breadcrumb aria-label="Page navigation" noTrailingSlash>
                        <BreadcrumbItem href="/">Getting started</BreadcrumbItem>
                    </Breadcrumb>
                    <!-- TODO: Integrate this with the SPA router -->
                    <h1 style="margin-bottom: 1.5rem">Design &amp; build with Carbon</h1>
                </Column>
            </Row>

            <Row>
                <Column noGutter>
                    <Tabs aria-label="Tab navigation">
                        <Tab label="About"/>
                        <Tab label="Design"/>
                        <Tab label="Add Adjacency"/>
                        <Tab label="Settings"/>
                        <div class="tabbed-content" slot="content">
                            <Grid as fullWidth let:props>
                                <TabContent {...props}>
                                    <PeerTable/>
                                </TabContent>
                                <TabContent {...props}>
                                    <Row>
                                        <Column lg="{7}" md="{4}">
                                            <p>
                                                Rapidly build beautiful and accessible experiences. The
                                                Carbon kit contains all resources you need to get
                                                started.
                                            </p>
                                        </Column>
                                    </Row>
                                </TabContent>
                                <TabContent {...props}>
                                    <Row>
                                        <Column lg="{7}" md="{4}">
                                            <PeerForm/>
                                        </Column>
                                    </Row>
                                </TabContent>
                                <TabContent {...props}>
                                    <Row>
                                        <Column lg="{7}" md="{4}">
                                            <Select
                                                    bind:selected="{theme}"
                                                    labelText="Carbon theme"
                                                    style="margin-bottom: 1rem"
                                            >
                                                <SelectItem text="White" value="white"/>
                                                <SelectItem text="Gray 10" value="g10"/>
                                                <SelectItem text="Gray 90" value="g90"/>
                                                <SelectItem text="Gray 100" value="g100"/>
                                            </Select>
                                            <p>
                                                Carbon is IBM’s open-source design system for digital
                                                products and experiences. With the IBM Design Language
                                                as its foundation, the system consists of working code,
                                                design tools and resources, human interface guidelines,
                                                and a vibrant community of contributors.
                                            </p>
                                        </Column>
                                    </Row>
                                </TabContent>
                            </Grid>
                        </div>
                    </Tabs>
                </Column>
            </Row>
            <Footer/>
        </Grid>
        {/if}
    </Content>
</Theme>
