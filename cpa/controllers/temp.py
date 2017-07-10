__author__ = 'Tien'

@auth.requires_signature()
def create_product():
    form = get_form()
    if form.accepts(request, session):
        try:
            try:
                class_id = db(db.clsb_class.class_code.like("None")).select()
                subject_class = None
                cat_id = request.vars.category
                if len(class_id) > 0:
                    class_id = class_id.first().id
                else:
                    class_id = db.clsb_class.insert(
                        class_name="Khác",
                        class_code="None",
                        class_order="9999",
                    )
                    class_id = class_id.id
                if request.vars.category == "0":
                    cat_id = db(db.clsb_category.category_code.like("None")).select()
                    if len(cat_id) <= 0:
                        cat_id = db.clsb_category.insert(
                            category_name="Danh m?c khác",
                            category_code="None",
                            category_order="9999"
                        )
                        cat_id = db.clsb_category.insert(
                            category_name="Khác",
                            category_code="None",
                            category_order="9999",
                            category_parent=cat_id.id
                        )
                        cat_id = cat_id.id
                        device_shelf_check = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()
                        if len(device_shelf_check) <= 0:
                            db.clsb20_category_shelf_mapping.insert(
                                category_id=cat_id,
                                device_shelf_id=db(db.clsb_device_shelf.device_shelf_code.like("STK")).select().first()['id']
                            )
                    else:
                        cat_id = cat_id.first().id

                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()
                    if len(subject_class) > 0:
                        subject_class = subject_class.first()
                    else:
                        subject_class = db.clsb_subject_class.insert(
                            subject_id=request.vars.subjects,
                            class_id=class_id
                        )
                else:
                    map = db(db.clsb20_category_class_mapping.category_id == request.vars.category).select()
                    if len(map) > 0:
                        class_id = map.first().class_id
                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()[0]
            except Exception as e:
                response.flash = "Có l?i x?y ra: l?a ch?n danh m?c sách không t??ng ?ng v?i môn h?c: "+str(e)+" - on line "+str(sys.exc_traceback.tb_lineno)
                return dict(form=form)
            code = usercp.user_gen_product_code(user_cp_path, db(db.clsb20_product_type.type_name.like("Book")).select()[0].type_code)
            result_str = ""
            create_dir(user_cp_path+"/upload/"+code)
            if request.vars.data != "":
                if request.vars.data.file:
                    if not bool(re.search(".[Zz][Ii][Pp]$", request.vars.data.filename)):
                        response.flash = "T?p tin ZIP không ?úng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    save_data(request.vars.data, code+"/"+code+".zip", code)
                    try:
                        zip_file = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "r")
                        for name in zip_file.namelist():
                            if bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                                f = zip_file.open(name)
                                print "Name "+ name
                                save_file(f, code+"/cover.clsbi")
                                f.close()
                                break

                        zip_file.close()
                    except Exception as e:
                        response.flash = "C?u trúc t?p tin ZIP không ?úng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                # if request.vars.cover != "":
                #     if request.vars.cover.file:
                #             save_file(request.vars.cover.file, code+"/cover.clsbi")

            elif request.vars.data_pdf != "":
                if request.vars.cover != "":
                    if not bool(re.search(".[Pp][Dd][Ff]$", request.vars.data_pdf.filename)):
                        response.flash = "T?p tin PDF không ?úng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    create_product_pdf(request, code)
                else:
                    response.flash = "D? li?u t?i lên thi?u ?nh bìa"
                    shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                    return dict(form=form)
            try:
                shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/thumb.png")
            except Exception as e:
                response.flash = "D? li?u t?i lên thi?u ?nh bìa"
                shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                return dict(form=form)
            # if request.vars.thumbnail != "":
            #     if request.vars.thumbnail.file:
            #             save_file(request.vars.thumbnail.file, code+"/thumb.png")
            if request.vars.f_info != "":
                osFileServer = OSFS("/tmp/")
                osFileServer.setcontents("product_info.xlsx", request.vars.image.f_info)

            creator_list = re.split(r"[,;]", request.vars.creator)
            creator = dict()
            add_creator = ""
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
            for creat in creator_list:
                if creat != "":
                    if add_creator == "":
                        creator = db(db.clsb20_dic_creator_cp.creator_name == creat).select()
                        add_creator = creat
                    else:
                        db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=code, metadata_value=creat)

            if len(creator) <= 0:
                creator = db.clsb20_dic_creator_cp.insert(creator_name=add_creator)
            else:
                creator = creator[0]

            publisher = db(db.clsb_dic_publisher.publisher_name == request.vars.publisher).select()

            if len(publisher) <= 0:
                publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
            else:
                publisher = publisher[0]


            device_shelf = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()[0]['device_shelf_id']

            newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
                                                  product_code=code,
                                                  product_description=request.vars.content,
                                                  subject_class=subject_class.id,
                                                  product_publisher=publisher.id,
                                                  product_creator=creator.id,
                                                  device_shelf_code=device_shelf,
                                                  product_category=cat_id,
                                                  product_price=request.vars.price)

            if request.vars.title_relation != "":
                list = request.vars.title_relation.split(";")
                sum = 0
                for one in list:
                    if (sum>0):
                        db.clsb20_product_relation_cp.insert(product_cp_id=newdata.id, relation_id=one)
                    sum = sum+1


            # if request.vars.creator_more != "":
            #     list_creator = re.split(r"[,;]",request.vars.creator_more)
            #     metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
            #     for one in list_creator:
            #         db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=one)

            if request.vars.year_created != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="pub_year", metadata_label="N?m xu?t b?n")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.year_created)

            price_cover = request.vars.price
            if request.vars.cover_price != "":
                price_cover = request.vars.cover_price
            metadata = db(db.clsb_dic_metadata.metadata_name.like("cover_price")).select()
            if len(metadata) <= 0:
                db.clsb_dic_metadata.insert(metadata_name="cover_price", metadata_label="Giá bìa")
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("cover_price")).select()[0]['id']
            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=price_cover)


            if request.vars.size_cover != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("format")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="format", metadata_label="Kích c?")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("format")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.size_cover)

            if request.vars.num_page != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="page_number", metadata_label="S? trang")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.num_page)

            if request.vars.payment != "":
                if request.vars.payment.upper() == "SUBSCRIPTIONS":
                    purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
                else:
                    purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                    purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

                db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)

            type_image = db(db.clsb20_image_type.name.like("Features")).select()
            if len(type_image) <= 0:
                type_image = db.clsb20_image_type.insert(name="Features", description="Features Images")
            else:
                type_image = type_image[0]
            for i in range(1, 6):
                if request.vars['feature_images_'+str(i)] != "":
                    try:
                        file = request.vars['feature_images_'+str(i)]
                        save_file(file.file, "clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                        db.clsb20_product_image.insert(type_id=type_image['id'], product_code=code, description=file.filename, image="clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                    except:
                        continue
            response.flash = 'Thành công'
        except Exception as e:
            print e
            response.flash = 'X?y ra l?i trong quá trình t?i lên'
    elif form.errors:
        response.flash = 'Thông tin không ?úng'
    else:
        response.flash = 'Xin m?i ?i?n vào form'
    return dict(form=form)
