import { describe, expect, test } from "@odoo/hoot";

import { loadDefaultAppWithDiplHomeMenu } from "../../src/webclient/webclient";

describe.current.tags("headless");

test("default app loader delegates to native webclient behavior", async () => {
    const webClient = { env: { services: {} } };
    const result = await loadDefaultAppWithDiplHomeMenu(webClient, async () => {
        expect.step("native");
        return "native";
    });

    expect(result).toBe("native");
    expect.verifySteps(["native"]);
});
