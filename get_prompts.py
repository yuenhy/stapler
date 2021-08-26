from prompts import make_prompts

# aw, pp, runs
# for 50 artworks, make 5 prompts
# run each prompt 5 times

print(make_prompts("catalogue.csv", "prompt_reference_list.csv", aw=50, pp=5, runs=5))