CREATE OR REPLACE PACKAGE TJX_RMS13EU.CORESVC_UCADJ AUTHID CURRENT_USER AS

  template_key      CONSTANT VARCHAR2(255) := 'TJX_UC_ADJ_UPLD';
  template_category CONSTANT VARCHAR2(255) := 'RMSFIN';

  action_new VARCHAR2(25) := 'NEW';
  action_mod VARCHAR2(25) := 'MOD';
  action_del VARCHAR2(25) := 'DEL';

  UCADJ_sheet VARCHAR2(255) := 'TJX_UC_ADJ';

  TJX_UC_ADJ$Action          NUMBER := 1;
  TJX_UC_ADJ$ADJ_NUMBER      NUMBER := 2;
  TJX_UC_ADJ$DEPT            NUMBER := 3;
  TJX_UC_ADJ$TJX_STYLE       NUMBER := 4;
  TJX_UC_ADJ$REASON          NUMBER := 5;
  TJX_UC_ADJ$QTY             NUMBER := 6;
  TJX_UC_ADJ$RETAIL          NUMBER := 7;
  TJX_UC_ADJ$LOCATION        NUMBER := 8;
  TJX_UC_ADJ$VENDOR_ORDER_NO NUMBER := 9;
  TJX_UC_ADJ$PROCESSING_AREA NUMBER := 10;
  TJX_UC_ADJ$KTR_NUM         NUMBER := 11;
  TJX_UC_ADJ$LANDED_COST     NUMBER := 12;
  TJX_UC_ADJ$STATUS          NUMBER := 13;

  action_column VARCHAR2(255) := 'ACTION';

  TYPE UCADJ_rec_tab IS TABLE OF tjx_uc_adj%ROWTYPE;

  sheet_name_trans S9T_PKG.trans_map_typ;

  -------------------------------------------------------------------------------------------------------
  FUNCTION CREATE_S9T(O_error_message     IN OUT RTK_ERRORS.RTK_TEXT%TYPE,
                      O_file_id           IN OUT S9T_FOLDER.FILE_ID%TYPE,
                      I_template_only_ind IN CHAR DEFAULT 'N') RETURN BOOLEAN;

--------------------------------------------------------------------------------------------------------
END CORESVC_UCADJ;
/

CREATE OR REPLACE PACKAGE BODY TJX_RMS13EU.CORESVC_UCADJ AS

  PROCEDURE INIT_S9T(O_file_id IN OUT NUMBER) IS
    L_file      s9t_file;
    L_file_name s9t_folder.file_name%TYPE;
  
  BEGIN
    L_file              := NEW s9t_file();
    O_file_id           := s9t_folder_seq.NEXTVAL;
    L_file.file_id      := O_file_id;
    L_file_name         := template_key || '_' || GET_USER || '_' ||
                           SYSDATE || '.ods';
    L_file.file_name    := L_file_name;
    L_file.template_key := template_key;
    L_file.user_lang    := GET_USER_LANG;
    L_file.add_sheet(UCADJ_sheet);
    L_file.sheets(L_file.get_sheet_index(UCADJ_sheet)).column_headers := S9T_CELLS('ACTION',
                                                                                   'ADJ_NUMBER',
                                                                                   'DEPT',
                                                                                   'TJX_STYLE',
                                                                                   'REASON',
                                                                                   'QTY',
                                                                                   'RETAIL',
                                                                                   'LOCATION',
                                                                                   'VENDOR_ORDER_NO',
                                                                                   'PROCESSING_AREA',
                                                                                   'KTR_NUM',
                                                                                   'LANDED_COST',
                                                                                   'STATUS');
  
    S9T_PKG.SAVE_OBJ(L_file);
  END INIT_S9T;

  ---------------------------------------------------------------- 
  PROCEDURE POPULATE_UCADJ(I_file_id IN NUMBER) IS
  BEGIN
    INSERT INTO TABLE
      (SELECT ss.s9t_rows
         FROM s9t_folder sf, TABLE(sf.s9t_file_obj.sheets) ss
        WHERE sf.file_id = I_file_id
          AND ss.sheet_name = UCADJ_sheet)
      SELECT s9t_row(s9t_cells(CORESVC_UCADJ.action_mod,
                               ADJ_NUMBER,
                               DEPT,
                               TJX_STYLE,
                               REASON,
                               QTY,
                               RETAIL,
                               LOCATION,
                               VENDOR_ORDER_NO,
                               PROCESSING_AREA,
                               KTR_NUM,
                               LANDED_COST,
                               STATUS))
        FROM tjx_uc_adj WHERE status = 'A';
        
  END POPULATE_UCADJ;

  ----------------------------------------------------------------------
  FUNCTION CREATE_S9T(O_error_message     IN OUT RTK_ERRORS.RTK_TEXT%TYPE,
                      O_file_id           IN OUT S9T_FOLDER.FILE_ID%TYPE,
                      I_template_only_ind IN CHAR DEFAULT 'N') RETURN BOOLEAN IS
    L_program VARCHAR2(64) := 'CORESVC_UCADJ.CREATE_S9T';
    L_file    s9t_file;
  
  BEGIN
  
    INIT_S9T(O_file_id);
    /*IF S9T_PKG.POPULATE_LISTS(O_error_message,
                              O_file_id,
                              template_category,
                              template_key) = FALSE THEN
      RETURN FALSE;
    END IF;*/
  
    IF I_template_only_ind = 'N' THEN
      POPULATE_UCADJ(O_file_id);
      COMMIT;
    END IF;
  
    S9T_PKG.APPLY_TEMPLATE(O_file_id, template_key);
  
    L_file := S9T_FILE(O_file_id);
    IF S9T_PKG.CODE2DESC(O_error_message, template_category, L_file) =
       FALSE THEN
      RETURN FALSE;
    END IF;
    S9T_PKG.SAVE_OBJ(L_file);
    S9T_PKG.UPDATE_ODS(L_file);
    RETURN TRUE;
  
  EXCEPTION
    WHEN OTHERS THEN
      O_error_message := SQL_LIB.CREATE_MSG('PACKAGE_ERROR',
                                            SQLERRM,
                                            L_program,
                                            TO_CHAR(SQLCODE));
      RETURN FALSE;
  END CREATE_S9T;

-------------------------------------------------------------

END CORESVC_UCADJ;
/
