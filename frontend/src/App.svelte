<script>
    import {Breadcrumb, BreadcrumbItem, Column, Content, Grid, Row, Select, SelectItem, Tab, TabContent, Tabs} from "carbon-components-svelte";
    import Header from "./components/Header.svelte";
    import Theme from "./components/Theme.svelte";
    import Footer from "./components/Footer.svelte";
    import PeerForm from "./components/PeerForm.svelte";
    import PeerTable from "./components/PeerTable.svelte";
    import {onMount} from "svelte";
    import {config} from "./stores";
    import Routers from "./pages/Routers.svelte";

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
    {#if ready}
    <Header/>
    <Content style="background: none; padding: 1rem">

        <Grid>
            <Row>
                <Column lg="{16}">
                    <!-- TODO: Integrate this with the SPA router -->
                    <Breadcrumb aria-label="Page navigation" noTrailingSlash>
                        <BreadcrumbItem href="/">Getting started</BreadcrumbItem>
                    </Breadcrumb>
                    <h1 style="margin-bottom: 1.5rem">Network Overview</h1>
                </Column>
            </Row>

            <Row>
                <Column noGutter>
                    <Tabs aria-label="Tab navigation">
                        <Tab label="Sessions"/>
                        <Tab label="Routers"/>
                        <Tab label="Add Adjacency"/>
                        <Tab label="Settings"/>
                        <div class="tabbed-content" slot="content">
                            <Grid as fullWidth let:props>
                                <!-- Sessions -->
                                <TabContent {...props}>
                                    <PeerTable/>
                                </TabContent>

                                <!-- Routers -->
                                <TabContent {...props}>
                                    <Routers/>
                                </TabContent>

                                <!-- Add Adjacency -->
                                <TabContent {...props}>
                                    <Row>
                                        <Column lg="{7}" md="{4}">
                                            <PeerForm/>
                                        </Column>
                                    </Row>
                                </TabContent>

                                <!-- Settings -->
                                <TabContent {...props}>
                                    <Row>
                                        <Column lg="{7}" md="{4}">
                                            <Select bind:selected="{theme}" labelText="UI theme">
                                                <SelectItem text="White" value="white"/>
                                                <SelectItem text="Gray 10" value="g10"/>
                                                <SelectItem text="Gray 90" value="g90"/>
                                                <SelectItem text="Gray 100" value="g100"/>
                                            </Select>
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
    </Content>
    {/if}
</Theme>
