# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20140806164157) do

  create_table "allele_references", force: true do |t|
    t.integer "locus_id"
    t.string  "allele_name",        limit: 80
    t.string  "regular_expression", limit: 500
    t.string  "allele_sequence",    limit: 500
  end

  create_table "alleles", force: true do |t|
    t.integer "experiment_id"
    t.integer "primer_id"
    t.integer "person_id"
    t.integer "locus_id"
    t.integer "barcode_person_id"
    t.string  "name",              limit: 80
    t.string  "allele_base",       limit: 1
    t.integer "count"
    t.integer "forward_count"
    t.float   "forward_qual"
    t.float   "reverse_qual"
    t.boolean "is_minor"
    t.boolean "is_stutter"
    t.boolean "is_novel_allele"
    t.boolean "is_novel_flank"
    t.boolean "is_good"
    t.string  "novel_flank_name",  limit: 80
    t.string  "flank5",            limit: 100
    t.string  "flank3",            limit: 100
    t.string  "str_call",          limit: 500
  end

  create_table "ancestries", force: true do |t|
    t.integer "person_sample_id"
    t.integer "ethnicity_id"
    t.integer "geographic_id"
    t.string  "source_description", limit: 100
    t.float   "percent"
    t.boolean "self_reported"
  end

  add_index "ancestries", ["ethnicity_id"], name: "index_ancestries_on_ethnicity_id", using: :btree
  add_index "ancestries", ["person_sample_id"], name: "index_ancestries_on_person_sample_id", using: :btree

  create_table "attachments", force: true do |t|
    t.integer  "user_id"
    t.integer  "folder_id"
    t.string   "file_name",        limit: 1000
    t.integer  "internal_hash",    limit: 8
    t.text     "description"
    t.string   "file_type",        limit: 80
    t.string   "content_type",     limit: 80
    t.integer  "content_bytes"
    t.binary   "contents",         limit: 2147483647
    t.boolean  "is_parsed"
    t.float    "version"
    t.float    "codebase_version"
    t.datetime "updated_at"
  end

  create_table "attachments_parameters", id: false, force: true do |t|
    t.integer "attachment_id"
    t.integer "parameter_id"
  end

  add_index "attachments_parameters", ["attachment_id", "parameter_id"], name: "index_attachments_parameters_on_attachment_id_and_parameter_id", using: :btree

  create_table "attributes", force: true do |t|
    t.string "name", limit: 80
  end

  create_table "barcodes", force: true do |t|
    t.integer "panel_id"
    t.string  "name",         limit: 32
    t.string  "barcode_seq",  limit: 32
    t.string  "barcode_type", limit: 32
  end

  add_index "barcodes", ["barcode_seq"], name: "idx_barcodes_seqs", using: :btree
  add_index "barcodes", ["panel_id"], name: "idx_barcodes_panel", using: :btree

  create_table "calls", force: true do |t|
    t.integer "experiment_id"
    t.integer "locus_id"
    t.integer "sample_id"
    t.integer "quality_thresh"
    t.float   "minor_allele_frequency"
    t.integer "total_count"
    t.integer "forward_count"
  end

  add_index "calls", ["experiment_id"], name: "index_calls_on_experiment_id", using: :btree
  add_index "calls", ["locus_id"], name: "index_calls_on_locus_id", using: :btree
  add_index "calls", ["sample_id"], name: "index_calls_on_sample_id", using: :btree

  create_table "calls_comparisons", id: false, force: true do |t|
    t.integer "call_id"
    t.integer "comparison_id"
  end

  add_index "calls_comparisons", ["call_id"], name: "index_calls_comparisons_on_call_id", using: :btree
  add_index "calls_comparisons", ["comparison_id"], name: "index_calls_comparisons_on_comparison_id", using: :btree

  create_table "choices", force: true do |t|
    t.integer "attribute_id"
    t.string  "name",         limit: 80
  end

  create_table "comparisons", force: true do |t|
    t.integer "mixture_sample_id"
    t.integer "reference_sample_id"
    t.integer "tp_count"
    t.integer "fp_count"
    t.integer "fn_count"
    t.integer "tn_count"
    t.float   "mixture_ma_threshold"
    t.float   "reference_ma_threshold"
    t.float   "rmne"
    t.float   "likelihood_ratio"
  end

  create_table "ethnicities", force: true do |t|
    t.integer "geographic_id"
    t.string  "name",          limit: 80
    t.float   "lat"
    t.float   "lng"
  end

  create_table "experimenters", force: true do |t|
    t.integer "experiment_id"
    t.integer "person_id"
    t.string  "role"
    t.boolean "empcr"
    t.boolean "uncertain_empcr"
    t.boolean "seq"
    t.boolean "uncertain_seq"
  end

  add_index "experimenters", ["experiment_id"], name: "index_experimenters_on_experiment_id", using: :btree
  add_index "experimenters", ["person_id"], name: "index_experimenters_on_person_id", using: :btree

  create_table "experiments", force: true do |t|
    t.integer "instrument_id"
    t.integer "primer_panel_id"
    t.integer "folder_id"
    t.integer "attachment_id"
    t.string  "hash_name",              limit: 32
    t.string  "name",                   limit: 80
    t.boolean "is_mixture"
    t.string  "call_url",               limit: 160
    t.integer "final_lib_reads"
    t.integer "wells_with_isp"
    t.integer "live_isp"
    t.integer "filtered_polyclonal"
    t.string  "pcr",                    limit: 45
    t.string  "amp_lig_quant",          limit: 45
    t.date    "empcr_date"
    t.string  "template_amount_loaded", limit: 500
    t.string  "notes",                  limit: 1000
    t.date    "run_date"
  end

  add_index "experiments", ["folder_id"], name: "index_experiments_on_folder_id", using: :btree

  create_table "families", force: true do |t|
    t.string "name",   limit: 80
    t.string "source", limit: 80
  end

  create_table "folders", force: true do |t|
    t.integer  "parent_id"
    t.integer  "user_id"
    t.string   "name",        limit: 80
    t.string   "description", limit: 160
    t.integer  "level"
    t.datetime "updated_at"
  end

  create_table "frequencies", force: true do |t|
    t.integer "locus_id"
    t.integer "ethnicity_id"
    t.float   "allele_frequency"
    t.string  "source",           limit: 64
  end

  create_table "geographics", force: true do |t|
    t.string "region_name", limit: 80
  end

  create_table "images", force: true do |t|
    t.integer  "folder_id"
    t.integer  "user_id"
    t.integer  "associated_image_id"
    t.integer  "associated_attachment_id"
    t.string   "file_name",                limit: 1000
    t.integer  "internal_hash",            limit: 8
    t.text     "description"
    t.string   "image_type",               limit: 80
    t.string   "content_type",             limit: 80
    t.integer  "picture_bytes"
    t.binary   "picture",                  limit: 16777215
    t.float    "version"
    t.float    "codebase_version"
    t.datetime "created_at"
  end

  create_table "instruments", force: true do |t|
    t.string "name", limit: 80
  end

  create_table "kinship_training_modules", force: true do |t|
    t.integer "parameter_id"
    t.string  "name"
    t.binary  "estimator_degree",           limit: 2147483647
    t.binary  "estimator_relationship",     limit: 2147483647
    t.binary  "feature_class_relationship", limit: 16777215
    t.binary  "normalization",              limit: 16777215
    t.binary  "feature_class_degree",       limit: 16777215
  end

  create_table "kinships", force: true do |t|
    t.integer "relationship_id"
    t.integer "common_minor_alleles"
    t.integer "total_minor_alleles"
  end

  create_table "loci", force: true do |t|
    t.string  "name",       limit: 80
    t.string  "locus_type", limit: 8
    t.string  "chromosome", limit: 2
    t.string  "region",     limit: 45
    t.integer "position"
    t.boolean "exclude"
    t.string  "str_unit",   limit: 40
    t.string  "flank5",     limit: 500
    t.string  "snp_iub",    limit: 1
    t.string  "flank3",     limit: 500
    t.float   "fst"
  end

  create_table "loci_groups", force: true do |t|
    t.string "name", limit: 200
  end

  create_table "loci_loci_groups", id: false, force: true do |t|
    t.integer "locus_id"
    t.integer "loci_group_id"
  end

  add_index "loci_loci_groups", ["locus_id", "loci_group_id"], name: "index_loci_loci_groups_on_locus_id_and_loci_group_id", using: :btree

  create_table "locus_attributes", force: true do |t|
    t.integer "locus_id"
    t.string  "attribute_name",   limit: 45
    t.string  "attribute_choice", limit: 45
  end

  create_table "panel_loci", force: true do |t|
    t.integer "panel_id"
    t.integer "locus_id"
    t.integer "quality_thresh"
    t.integer "ambiguous",      default: 0
    t.integer "low",            default: 0
    t.integer "strand_bias",    default: 0
    t.integer "total_count",    default: 0
  end

  add_index "panel_loci", ["locus_id"], name: "index_panel_loci_on_locus_id", using: :btree
  add_index "panel_loci", ["panel_id"], name: "index_panel_loci_on_panel_id", using: :btree

  create_table "panels", force: true do |t|
    t.integer  "attachment_id"
    t.string   "name",          limit: 80
    t.string   "panel_type",    limit: 40
    t.string   "description",   limit: 80
    t.datetime "updated_at"
  end

  create_table "parameters", force: true do |t|
    t.integer "user_id"
    t.string  "group_name", limit: 40
    t.string  "category",   limit: 80
    t.string  "name",       limit: 80
    t.float   "value"
    t.boolean "is_visible"
  end

  create_table "people", force: true do |t|
    t.integer "best_sample_id"
    t.string  "id_code",                limit: 80
    t.string  "source",                 limit: 80
    t.text    "self_reported_ancestry"
  end

  create_table "person_samples", force: true do |t|
    t.integer "sample_id"
    t.integer "person_id"
    t.string  "molarity",  limit: 25
  end

  add_index "person_samples", ["person_id"], name: "index_person_samples_on_person_id", using: :btree
  add_index "person_samples", ["sample_id"], name: "index_person_samples_on_sample_id", using: :btree

  create_table "person_values", force: true do |t|
    t.integer "person_id"
    t.integer "attribute_id"
    t.integer "choice_id"
    t.string  "attribute_type",   limit: 16
    t.integer "attribute_int"
    t.float   "attribute_float"
    t.string  "attribute_string", limit: 80
    t.boolean "attribute_bool"
    t.string  "source",           limit: 80
    t.boolean "is_truth"
  end

  create_table "points", force: true do |t|
    t.integer "image_id"
    t.string  "type_of_point", limit: 32
    t.float   "qual"
  end

  create_table "primers", force: true do |t|
    t.integer "panel_id"
    t.integer "locus_id"
    t.string  "name",       limit: 80
    t.boolean "is_forward"
    t.string  "sequence",   limit: 500
  end

  create_table "relationships", force: true do |t|
    t.integer "family_id"
    t.integer "person_id"
    t.integer "person2_id"
    t.string  "relation",                limit: 64
    t.integer "degree"
    t.float   "expected_shared_alleles"
  end

  create_table "samples", force: true do |t|
    t.integer "experiment_id"
    t.integer "barcode_id"
    t.integer "quality_thresh"
    t.boolean "is_good"
    t.boolean "is_mixture"
    t.integer "minor_alleles_called", default: 0
    t.integer "total_reads",          default: 0
  end

  add_index "samples", ["barcode_id"], name: "index_samples_on_barcode_id", using: :btree
  add_index "samples", ["experiment_id"], name: "index_samples_on_experiment_id", using: :btree

  create_table "snps", force: true do |t|
    t.integer "call_id"
    t.string  "allele_base",  limit: 1
    t.integer "count"
    t.float   "forward_qual"
    t.float   "reverse_qual"
    t.boolean "is_minor"
  end

  add_index "snps", ["call_id"], name: "index_snps_on_call_id", using: :btree

  create_table "strs", force: true do |t|
    t.integer "experiment_id"
    t.integer "primer_id"
    t.integer "locus_id"
    t.integer "sample_id"
    t.string  "name",             limit: 80
    t.boolean "is_stutter"
    t.boolean "is_novel_allele"
    t.boolean "is_novel_flank"
    t.string  "novel_flank_name", limit: 80
    t.string  "flank5",           limit: 100
    t.string  "flank3",           limit: 100
    t.string  "str_call",         limit: 500
  end

  add_index "strs", ["experiment_id"], name: "index_strs_on_experiment_id", using: :btree
  add_index "strs", ["locus_id"], name: "index_strs_on_locus_id", using: :btree
  add_index "strs", ["primer_id"], name: "index_strs_on_primer_id", using: :btree
  add_index "strs", ["sample_id"], name: "index_strs_on_sample_id", using: :btree

  create_table "users", force: true do |t|
    t.integer "home_folder_id"
    t.string  "username",        limit: 10
    t.string  "name",            limit: 80
    t.string  "email",           limit: 80
    t.string  "hashed_password", limit: 64
    t.string  "salt",            limit: 64
    t.boolean "is_admin"
  end

end
