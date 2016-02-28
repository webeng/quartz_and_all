# Quart&All@HackConstruct

This project intends to do do a general health hazard analysis given a list of products used in a project. The list has to have valid Quartz ids for each product. We also provide potential product replacements for the most hazardous materials.

For example, a project has the following products:
* Membrane Roofing Adhesives
* Exterior Door w/ IGU
* Fiberglass Board Insulation
* more

#### 1 -  Product Name to Quartz Common Product Name
Then you have to map the specified products with the Quartz database. Therefore, the list will look like this:
`target_product_ids = ['CP126-a00','CP072-a01','CP179-a00']`

#### 2 - Health Hazard Visualization
The following methods will generate a couple of plots that show how many health hazards are in the project
`qA.plotHazardsCounter(target_product_ids,)
df = qA.plotHazardsHist(target_product_ids)`

![Health & Safety Hazards Before](https://github.com/webeng/quartz_and_all/blob/master/plots/health_and_safety_hazards_before.png "Health & Safety Hazards Before")

![Health & Safety Hazards After](https://github.com/webeng/quartz_and_all/blob/master/plots/health_and_safety_hazards_after.png "Health & Safety Hazards After")

The scatter plot shows you the hazzards. The objective is to keep all the hazards as close to zero as possible.

#### 3 - Identify Top Health Hazards
Then you want to run `createRankedListToMitigate` to get a ranked list of potential hazards to mitigate. 

#### 4 - Optimisation: Search For Replacements or Subsiture materials
The next step is to look at the list and try to reduce the number of hazards that are at the top of the list.
To do that, we are going to generate search queries to find real manufacturers and prodcuts using SpecifiedBy bulding product database or Google. Run `quarts2ProductsAndManufacturers` to generate search queries to find products and manufacturers.

The spreadsheet `how_to_mitigate_hazards.xlsx` also gives you ideas about how you can reduce health hazards.

#### Extra 5 - Update product data and visualise again
Once you find replacements, you can update the quartz data for that product using the replacement information. Note that, this is a very hacky way to do it but we didn't have more time to do it in a better way.

During the hackathon, we only focused on top hazards but there is plenty of room for improvement. We focused on: Exterior Door w/ IGU, Membrane roofing adhesives, Fiberglass Board Insulation, Ready Mix Concrete (Fly Ash) (3,000 - 4,000 psi) and EPDM membrane roofing

Some replacements we did:
* We found more sustainable roofing adhesives than the one currently specified.
* We found more sustainable fiberglass board insulation than the one currently specified.
* Replaced specified doors for timber doors.
* Replaced concrete for timber. Quite a big replacement but it turns out that Timber is healthier than concrete.