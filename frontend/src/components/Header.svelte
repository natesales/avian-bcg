<script>
    import {Header, HeaderGlobalAction, HeaderUtilities, SkipToContent} from "carbon-components-svelte";
    import Notification20 from "carbon-icons-svelte/lib/Notification20";
    import UserAvatar20 from "carbon-icons-svelte/lib/UserAvatar20";
    import AppSwitcher20 from "carbon-icons-svelte/lib/AppSwitcher20";
    import {getContext} from "svelte";
    import {config} from "../stores";

    const ctx = getContext("Theme");

    $: if (ctx) {
        ctx.dark.subscribe((value) => {
            console.log("dark mode?", value);
        });
        ctx.light.subscribe((value) => {
            console.log("light mode?", value);
        });
        ctx.updateVar("--cds-productive-heading-06-font-size", "4rem");
    }
</script>

<Header company={$config.network.name + " AS" + $config.network.asn} href="/" platformName="AVIAN Network Dashboard">
    <div slot="skip-to-content">
        <SkipToContent/>
    </div>
    <HeaderUtilities>
        <HeaderGlobalAction aria-label="Notifications" icon="{Notification20}"/>
        <HeaderGlobalAction aria-label="User Avatar" icon="{UserAvatar20}"/>
        <HeaderGlobalAction aria-label="App Switcher" icon="{AppSwitcher20}"/>
    </HeaderUtilities>
</Header>
