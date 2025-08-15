describe("Home page", () => {
  it("loads successfully", () => {
    cy.visit("/");
    cy.contains("App 1");
  });
});
