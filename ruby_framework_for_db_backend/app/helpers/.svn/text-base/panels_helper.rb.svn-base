module PanelsHelper
  def panel_data_link(panel)
    case panel.panel_type
      when "Barcodes"
        link_to(number_with_delimiter(Barcode.where(panel_id: panel.id).count), barcodes_path(panel_id: panel.id) )
      when "Primers"
        link_to(number_with_delimiter(Primer.where(panel_id: panel.id).count), primers_path(panel_id: panel.id))
      when "SNP References"
        link_to(number_with_delimiter(PanelLocus.where(panel_id: panel.id).count), loci_path(panel_id: panel.id))
      else
        ''
    end
  end

end
