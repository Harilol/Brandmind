from schemas import DiscoverOutput

# Valid data should work
good = DiscoverOutput(
    core_problem="Students struggle to find compatible project teammates",
    target_user="University CS students",
    context="Academic group projects",
    constraints=["No budget", "Must work on mobile"],
    core_value="Faster, better-matched team formation",
    open_questions=["Is this for undergrads only?"]
)
print("Valid OK:", good.core_problem)

# Invalid data should raise an error
try:
    bad = DiscoverOutput(
        core_problem="x",
        target_user="y",
        context="z",
        constraints="this should be a list, not a string",
        core_value="w",
        open_questions=[]
    )
    print("ERROR: should have failed")
except Exception as e:
    print("Validation caught the bad shape:", type(e).__name__)