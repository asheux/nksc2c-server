import re
import json

from create_app import app
from nksc2c.models import NKS, db, StatusEnum


IMAGES_JSON = "images.json";
NEW_IMAGES_JSON = "newimages.json";
TO_APPROVE = [
    "page0024a_ca.1",
    "page0024b_ca.2",
    "page0024c_ca_rule",
    "page0027a_rule30-ca",
    "page0025a_rule250-ca",
    "page0025c_rule90-ca",
    "page0025d_rule90-rule",
    "page0026a_fractal",
    "page0027a_rule30-ca",
    "page0029a_rule30-ca",
    "page0030a_rule30-ca",
    "page0032a_rule110-ca",
    "page0038a_rule110-big.6",
    "page0052a_rule_250_90_30_110",
    "page0053a_rule_250_90_30_110",
    "page0054a_diff_rules_evol.1",
    "page0055a_diff_rules_evol.2",
    "page0056a_diff_rules_evol.3"
    "page0058a_fractal_patterns-ca",
    "page0059a_rule_30_45_73-ca",
    "page0061a_seq_totalistic-ca",
    "page0062a_3c_totalistic_rule-ca.1",
    "page0063a_3c_totalistic_rule-ca.2",
    "page0063b_3c_totalistic_rule-ca.3",
    "page0064a_3c_totalistic_rule-ca.4",
    "page0066a_3c_totalistic_rule-ca.5",
    "page0067a_code1635-ca",
    "page0068a_code2049-ca",
    "page0069a_growth_extinction-ca",
    "page0070a_code1599-ca",
    "page0071a_small-ma",
    "page0071b_small_rule-ma",
    "page0072a_squareroot_2t-ma",
    "page0072b_squareroot_2t_rule-ma",
    "page0072c_compressed_gh-ma",
    "page0073a_200_steps-ma",
    "page0073b_200_steps_rule-ma",
    "page0073c_small-ma",
    "page0073d_compressed-ma",
    "page0074a_random_ft_rule-ma",
    "page0074b_random_ft_c-ma",
    "page0074c_random_ft-ma",
    "page0075a_srw-ma",
    "page0075b_srw_compressed-ma",
    "page0075c_srw_rule-ma",
    "page0076b_generalized-ma",
    "page0076a_generalized_rule-ma",
    "page0077e_xma.seq.abcdefgh-rules",
    "page0078a_tm",
    "page0078b_tm.rule",
    "page0082a_ss.evol",
    "page0083a_ss.evol.abcd",
    "page0084a_ni_ss.evol",
    "page0084b_ni_ss.rules",
    "page0084c_ss.trees",
    "page0089a_simple_ss.seq",
    "page0090a_ss_2replacmnt.rule",
    "page0090b_ss_2replacmnt.seq",
    "page0091a_ss_3replacmnt.seq",
    "page0091b_ss_3replacmnt.rules",
    "page0092a_ss_random.seq.1",
    "page0092b_ss_random.seq.2",
    "page0092c_ss_compressed.seq.3",
    "page0092d_ss_random.rule",
    "page0104a_diff_symbolic_s.evol",
    "page0107a_varying_complexity-ca",
    "page0116a_number3829_bases",
    "page0121a_base2_succ_powers3.2",
    "page0122a_3.2_fractional_sizes",
    "page0122b_results_starting.1",
    "page0122c_base2_succ.p.3.2",
    "page0125a_base2_start.16",
    "page0128a_simple_recursive.seq",
    "page0129a_seq.1",
    "page0129b_graph.2",
    "page0130a_fluctuations",
    "page0132a_prime_no_process",
    "page0136a_pictorial_rep",
    "page0139a_rational_numbers.2",
    "page0141a_root_gen_procedure",
    "page0150a_iterated_maps.1",
    "page0150b_iterated_maps.2",
    "page0150c_iterated_maps.3",
    "page0151a_iterated_m_PI4.1",
    "page0151b_iterated_m_PI4.2",
    "page0151c_iterated_m_PI4.3",
    "page0153a_shift_map",
    "page0153b_shift_map.effect",
    "page0155a_dff_dig_seq",
    "page0157a_continuous-ca-rule",
    "page0157b_continuous-ca",
    "page0158a_c-grid-constant.1.4",
    "page0158c_c-constant.1.4.rule",
    "page0159a_c-diff-constant-ca",
    "page0160a_c-diff-constant-more",
    "page0170a_2d.ca",
    "page0171b_code942",
    "page0171a_code1022",
    "page0172a_3d_of_2d_stack",
    "page0173a_2d_patterns_seq.ca.1",
    "page0174a_2d_patterns_seq.ca.2",
    "page0175a_1d_patterns_seq",
    "page0177a_code175850.1",
    "page0177b_code175850.2",
    "page0177c_code175850.3",
    "page0177d_code175850.rule",
    "page0178a_circle_pattern.ca",
    "page0179a_code174826.ca",
    "page0181a_row11_ca.100",
    "page0181b_row11_ca.200",
    "page0181c_row11_ca.300",
    "page0181d_row11_ca.400",
    "page0181e_row11_ca.500",
    "page0183a_3d_ca.1",
    "page0183b_3d_ca.2",
    "page0188a_2d_bigss",
    "page0190c_geometrical.ss.rule",
    "page0191a_fractal_pats.1",
    "page0191b_fractal_pats.2",
    "page0191e_fractal_pats.3",
    "page0191c_fractal_pats.4",
    "page0191d_fractal_pats.5",
    "page0210a_sboc_blackwhite",
    "page0211a_sboc_blackwhite.2",
    "page0212a_fixed_num_bw",
    "page0213a_match_colors",
    "page0219a_simplest_system.1",
    "page0219b_simplest_system.2",
    "page0219c_simplest_s.rule",
    "page0220a_3by3templates.rule",
    "page0220b_3by3templates",
    "page0221a_56_3by3template.1",
    "page0221b_56_3by3templates.2",
    "page0221c_56_3by3.rule",
    "page0231a_four_classes",
    "page0232a_symmetrical.ca",
    "page0233a_totalistic.ca",
    "page0234a_3color_totalistic.ca",
    "page0236a_big_3c_totalistic.ca"
    "page0237a_3ct_code2007.ca",
    "page0238a_3ct_code1659.ca",
    "page0239a_3ct_code2043.ca",
    "page0240a_borderline.ca",
    "page0241a_seq_totalistic.rules",
    "page0243a_evol_random_init.ca",
    "page0244a_class4hehvior.ca",
    "page0246a_2d_totalistic_rules.ca",
    "page0247a_2d_seq_totalistic.ca",
    "page0248a_1d_thru_2d.ca.1",
    "page0248b_1d_thru_2d.ca.2",
    "page0249a_class4_2d.ca.1",
    "page0249b_class4_2d.ca.2",
    "page0250a_color_change.ca",
    "page0251a_3typical_class3.ca",
    "page0253a_rule110_class4.ca",
    "page0254a_1cellchanged.ca",
    "page0255a_six_possible_pos",
    "page0257a_double_each_step.1",
    "page0257b_double_each_step.2",
    "page0259a_rule90_30.ca",
    "page0260a_function_size.ca.1",
    "page0260b_function_size.ca.2",
    "page0260c_function_size.ca.3",
    "page0260d_function_size.ca.4",
    "page0261a_rule30_rand_init.ca",
    "page0262a_rule22_rand_init.ca",
    "page0263a_rule22_diff_sinit.ca",
    "page0264a_rule90_vinitcond.ca",
    "page0265a_evol_frandinitcond.ca",
    "page0266a_sic_rule30.ca",
    "page0267a_rule126_randinit.ca",
    "page0268a_rule30_patterns.ca",
    "page0269a_sic_rule126.ca",
    "page0269b_sic_rule126.rule",
    "page0270a_sic_rule90.ca",
    "page0270b_sic_rule90.rule",
    "page0271a_sic_rule150.ca",
    "page0271b_sic_rule150.rule",
    "page0271c_sic_rule184.ca",
    "page0271d_sic_rule184.rule",
    "page0272a_rule184_ninitc.ca",
    "page0272b_rule184_ninitc.rule",
    "page0273a_rule184_frandinit.ca",
    "page0274a_nested_pat_rinic.ca",
    "page0275a_attractor_seq.ca-rule",
    "page0276a_final_state_rule4.ca",
    "page0282a_three_class4.ca",
    "page0283a_code_20_diff.ca",
    "page0284a_p_code20.ca.1",
    "page0285a_p_code20.ca.2",
    "page0286a_p_code357.ca",
    "page0287a_p_code1329.ca",
    "page0288a_unbounded_code1329.1",
    "page0289a_unbounded_code1329.2",
    "page0290a_rule110_randinitc.ca",
    "page0292a_p_rule110.ca",
    "page0293a_unbounded_rule110.ca",
    "page0294a_collisions.ca.1",
    "page0295a_collisions.ca.2",
    "page0296a_collisions.ca.3",
    "page0299a_rand_mechanism.1",
    "page0299b_rand_mechanism.2",
    "page0299c_rand_mechanism.3",
    "page0305a_rolled_balls_rep",
    "page0305b_rolled_balls",
    "page0307a_kneading_process",
    "page0307b_nearby_points.kp",
    "page0308a_digit_sequences.kp",
    "page0311a_mirror_arrangement",
    "page0311b_machine-big.rule",
    "page0312a_4_ideal_balls.r",
    "page0312b_4_ideal_balls.path",
    "page0315a_rule30_irg.ca",
    "page0319a_base2_digits_pat",
    "page0320a_linear.crng.1a",
    "page0320b_multiplier3.1b",
    "page0320c_2d_linear.crng.1c",
    "page0320d_3d_linear.crng.1d",
    "page0320e_linear.crng.2a",
    "page0320f_multiplier37.2b",
    "page0320g_2d_linear.crng.2c",
    "page0320h_3d_linear.crng.2d",
    "page0320i_linear.crng.3a",
    "page0320j_multiplier65539.3b",
    "page0320k_2d_linear.crng.3c",
    "page0320l_3d_linear.crng.3d",
    "page0324a_rule30_2-3.ca",
    "page0325a_perturbations.1",
    "page0325b_perturbations.2",
    "page0329a_random_walks",
    "page0329b_random_walks.gaus",
    "page0334a_2dimensional.ca.1",
    "page0334b_2dimensional.ca.2",
    "page0334c_2dimensional.ca.3",
    "page0335a_random_fluctuations",
    "page0338a_discrete_c.1d.ca.1",
    "page0338b_discrete_c.1d.ca.2",
    "page0339a_density_1d.ca.1",
    "page0339b_density_1d.ca.2",
    "page0341a_continuous_system",
    "page0346a_results",
    "page0346b_example_curves",
    "page0347a_results_mode",
    "page0348a_2of28elem.ca",
    "page0352a_seqofelem.ca",
    "page0354a_uniform_behaviour",
    "page0354b_uniformly_b-w",
    "page0355a_closed_curve",
    "page0355b_localized_ca-ma",
    "page0355c_time_space_wave",
    "page0355d_space&time.ca",
    "page0356a_r50.r54.r62.ca",
    "page0356b_rule184",
    "page0356c_rule110_behaviour",
    "page0358a_r90-r150_nested",
    "page0358b_nested_patterns",
    "page0359a_nested_rule184",
    "page0359b_r110_compressed.evol",
    "page0360a_apprandomness",
    "page0369a_faceted_form.ca.1",
    "page0369b_faceted_form.ca.2",
    "page0371a_hexagonal.grid",
    "page0375a_frature.ca",
    "page0382a_rule225.fflow.ca",
    "page0382b_rule225.fflow.rule",
    "page0391a_rand_mutations.ca",
    "page0398a_example.ca",
    "page0400a_sub_sys.gplants",
    "page0411a_damping.change",
    "page0411b_geometries",
    "page0411c_diff_angles.pat",
    "page0412a_ddist_center.disks",
    "page0413a_idealized_horns",
    "page0424a_symmetrical.ca.pat",
    "page0427a_2d_evolution.ca",
    "page0428a_patterns.grid",
    "page0429a_diff_wheight.rules",
    "page0432a_buy_or_sell.model",
    "page0432b_b-or-s.model.rule",
    "page0432c_b-or-s.model.graph",
    "page0435a_rule_51-254.ca",
    "page0436a_reversible.6.ca",
    "page0436b_1800_reversible.ca",
    "page0437a_set.reversible.ca",
    "page0437b_st.reversible.rule",
    "page0438a_r_reversible.ca.1",
    "page0438b_r_reversible.ca.2",
    "page0439a_3reversible.ca",
    "page0440a_loc.rev.ca",
    "page0442a_rule122R.ca.1",
    "page0443a_rule122R.ca.2",
    "page0451a_eqilb.r122R.ca",
    "page0452a_v.rs.rev.ca",
    "page0454a_rule37R.ca",
    "page0456a_rule37R.r.ca",
    "page0458a_elem.ca",
    "page0459a_nnn_rules.ca",
    "page0462a_rule.c-d",
    "page0463a_block.ca",
    "page0467b_rule94.ca",
    "page0473a_fgrid.2d.ca",
    "page0476a_nodes.decomp",
    "page0485a_1d_symm.ca",
    "page0487a_global.sync.ma",
    "page0525a_class4.ca",
    "page0526a_code294.1893.ca",
    "page0526b_irrc_lines.net",
    "page0527a_K5K3.3.net",
    "page0527b_K3.3_embed.net",
    "page0533a_trivalent.net",
    "page0540a_r110_class4.ca",
    "page0549a_percept.summary",
    "page0551a_totalistic.ca",
    "page0553a_dd_randomness",
    "page0558a_q.rand.q.complex",
    "page0561a_runlen.encoding.1",
    "page0561b_runlen.encoding.2",
    "page0562a_runlen.encoding.ca",
    "page0563a_Huffman.coding.1",
    "page0563b_H.coding.rules",
    "page0564a_Huffman.coding.ca",
    "page0565a_pointer.based.enc",
    "page0567a_pb_encoding.ca",
    "page0568a_2d_rec_subd.1",
    "page0568b_2d_rec_subd.2",
    "page0569a_2d_bp.encoding",
    "page0569b_rule30.rule",
    "page0569c_r30.3x2blocks",
    "page0572a_nested_squares",
    "page0573a_2d_Walsh.funcs",
    "page0575a_fractions.set_bf",
    "page0578a_1d_ca.patches",
    "page0579a_2x2template",
    "page0580a_loc_arrangemnt",
    "page0581a_16possible2x2",
    "page0582a_2x2_3x3blocks",
    "page0583a_np_2d_subsys",
    "page0584a_approx.randmnes",
    "page0585a_discrt.elem.seq",
    "page0587a_freq_spectra",
    "page0590a_prob_models.nets",
    "page0591a_prob.ca.rule",
    "page0591b_probablstc.ca.1",
    "page0591c_probablstc.ca.2",
    "page0592a_comp.oca-probca",
    "page0594a_stats_block.seq.1",
    "page0594b_stats_block.seq.2",
    "page0597a_diff.evol.ca",
    "page0598a_encrypt_scheme.0",
    "page0599a_key_cycling",
    "page0600a_r60_ca.encrypn",
    "page0601a_additive.ca.cryt",
    "page0602a_rule60.ca.add",
    "page0602b_r60.ca.more",
    "page0603a_r30_encrypt.seq",
    "page0604a_sw_evol_r30.ca",
    "page0604b_sw_evol_r30.rules",
    "page0608a_simpl_math_proc.1",
    "page0608c_simpl_math_proc.3",
    "page0608b_sm_proc.2.rules",
    "page0610a_algebraic_rep",
    "page0611a_arithmetic.op",
    "page0613a_s_math_formula.1",
    "page0613b_s_math_formula.2",
    "page0613c_s_math_formula.3",
    "page0614a_successive.mul",
    "page0614b_mul.ca",
    "page0614c_multplr3_base6",
    "page0614d_base10_mul2-5",
    "page0615a_powers.compute",
    "page0624a_hash_codes.gen",
    "page0638a_compute_rem.ca",
    "page0638b_compute_rem.rule",
    "page0639a_compute_square.ca",
    "page0640a_compute_primes.ca.1",
    "page0640b_compute_primes.ca.2",
    "page0641a_computation.math",
    "page0641b_not_computation",
    "page0645a_urule254.ca.1",
    "page0645b_urule254.ca.2",
    "page0645c_urule254.rule",
    "page0646a_urule90.ca.1",
    "page0646b_urule90.rule",
    "page0646c_urule90.ca.2",
    "page0647a_urule30.ca.1",
    "page0647b_urule30.ca.2",
    "page0647c_urule30.rule",
    "page0653a_unextnnn.ca",
    "page0653b_unextnnn.rule",
    "page0655a_tot.code1599.ca.1",
    "page0655b_tot.code1599.ca.2",
    "page0655c_tot.code1599.rule",
    "page0676a_rule110.rule",
    "page0738a_crirr.evol.ca",
    "page0740a_5000s.evol.ca",
    "page0745a_example.pat",
    "page0747a_example_pats",
    "page0750a_analog_free_w.ca",
    "page0754a_undecidablty.ca",
    "page0803a_axiom_sys",
    "page0830a_rule110-30.ca",
    "page0831a_rule254-30.ca",
    "page0832a_width_doubln.ca",
    "page0833a_w_doubln.3c.ca.1",
    "page0833b_w_doubln.3c.ca.2",
]

try:
    with open(IMAGES_JSON, "r") as fd:
        json_data = json.load(fd)

    with open(NEW_IMAGES_JSON, "r") as fd2:
        json_data2 = json.load(fd2)

    # Insert data into the database
    with app.app_context():
        records = []

        print("Stared saving images.")
        for jd in [json_data, json_data2]:
            for page_name, pixels in jd.items():
                nks = NKS.query.filter_by(page_name=page_name).first()
                pixel_to_string = json.dumps(pixels)
                if not nks:
                    nks = NKS(pixel_data=pixel_to_string, page_name=page_name)
                else:
                    nks.pixel_data = pixel_to_string
                records.append(nks)

        db.session.bulk_save_objects(records)
        db.session.commit()
        print("Data inserted successfully!")

        # Approve all in TO_APPROVE
        to_save = []
        print("Started approving.")
        for notebook_name in TO_APPROVE:
            page_name = notebook_name.split('_')[0]
            nks = NKS.query.filter_by(page_name=page_name).first()
            if not nks or nks.status == StatusEnum.APPROVED:
                continue

            page = [int(sn) for sn in re.findall(r'\d+', notebook_name)][0] # will always have strinnum
            nks.name = "unknown"
            nks.status = StatusEnum.APPROVED
            nks.notebook_name = notebook_name
            nks.notebook_link = f"https://www.wolframscience.com/nks/p{page}"
            nks.upload_token = nks.generate_upload_token()
            to_save.append(nks)

        db.session.bulk_save_objects(to_save)
        db.session.commit()
        print("Approved notebooks successfully!")


except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    print(f"Error at line {e.lineno}, column {e.colno}, position {e.pos}")

